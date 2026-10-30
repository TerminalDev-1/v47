"""Early v69 private server: ClientHello and ServerHello only.

The hello layout is informed by the public laserjs v69 protocol client.
The Android client, post-hello encryption, and login remain unverified.
"""
import argparse
import asyncio
import logging
import secrets
import struct

LOG = logging.getLogger('private_server')
HEADER_SIZE = 7
MAX_PAYLOAD = 4 * 1024 * 1024
CLIENT_HELLO = 10100
SERVER_HELLO = 20100


def parse_client_hello(payload: bytes) -> dict:
    if len(payload) < 32:
        raise ValueError('truncated ClientHello')
    protocol, crypto, major, build, minor, hash_len = struct.unpack_from('>6i', payload)
    if hash_len < 0 or hash_len > 4096 or len(payload) != 32 + hash_len:
        raise ValueError('invalid ClientHello fingerprint length')
    fingerprint = payload[24:24 + hash_len].decode('utf-8')
    device, store = struct.unpack_from('>2i', payload, 24 + hash_len)
    return {'protocol': protocol, 'crypto': crypto, 'major': major,
            'build': build, 'minor': minor, 'fingerprint': fingerprint,
            'device': device, 'store': store}


def encode_frame(message_type: int, payload: bytes, version: int = 0) -> bytes:
    if len(payload) > 0xffffff:
        raise ValueError('payload exceeds frame limit')
    return (message_type.to_bytes(2, 'big') + len(payload).to_bytes(3, 'big') +
            version.to_bytes(2, 'big') + payload)


def decode_header(header: bytes) -> tuple[int, int, int]:
    if len(header) != HEADER_SIZE:
        raise ValueError('header must be exactly seven bytes')
    return (int.from_bytes(header[:2], 'big'),
            int.from_bytes(header[2:5], 'big'),
            int.from_bytes(header[5:], 'big'))


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info('peername')
    hello_received = False
    LOG.info('connection from %s', peer)
    try:
        while True:
            header = await asyncio.wait_for(reader.readexactly(HEADER_SIZE), 30)
            message_type, length, version = decode_header(header)
            if length > MAX_PAYLOAD:
                LOG.warning('invalid candidate frame size %s from %s', length, peer)
                break
            payload = await asyncio.wait_for(reader.readexactly(length), 30)
            LOG.info('frame type=%s bytes=%s version=%s from=%s',
                     message_type, length, version, peer)
            if message_type == CLIENT_HELLO:
                if hello_received:
                    LOG.warning('duplicate ClientHello from %s', peer)
                    break
                try:
                    hello = parse_client_hello(payload)
                except (ValueError, UnicodeDecodeError) as exc:
                    LOG.warning('invalid ClientHello from %s: %s', peer, exc)
                    break
                hello_received = True
                LOG.info('ClientHello client=%s.%s build=%s protocol=%s crypto=%s',
                         hello['major'], hello['minor'], hello['build'],
                         hello['protocol'], hello['crypto'])
                challenge = secrets.token_bytes(24)
                writer.write(encode_frame(SERVER_HELLO, struct.pack('>i', len(challenge)) + challenge))
                await writer.drain()
                LOG.info('ServerHello sent to %s', peer)
            else:
                LOG.info('message %s is not implemented yet', message_type)
    except asyncio.IncompleteReadError as exc:
        if exc.partial:
            LOG.info('connection closed with %d incomplete bytes from %s', len(exc.partial), peer)
    except (asyncio.TimeoutError, ConnectionError) as exc:
        LOG.info('connection ended from %s: %s', peer, type(exc).__name__)
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except ConnectionError:
            pass
        LOG.info('disconnected %s', peer)


async def main():
    parser = argparse.ArgumentParser(description='Private Server v69 handshake test server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=9339)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    server = await asyncio.start_server(handle_client, args.host, args.port)
    LOG.info('listening on %s; Android client and post-hello login are not yet verified',
             ', '.join(str(s.getsockname()) for s in server.sockets))
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
