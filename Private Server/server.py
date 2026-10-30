"""Protocol probe for the Brawl Stars v69 private server.

The older seven-byte Supercell frame is a hypothesis, not a verified v69
protocol. This probe records frame metadata and never sends invented replies.
"""
import argparse
import asyncio
import logging
import struct

LOG = logging.getLogger('private_server')
HEADER_SIZE = 7
MAX_PAYLOAD = 4 * 1024 * 1024


def decode_header(header: bytes) -> tuple[int, int, int]:
    if len(header) != HEADER_SIZE:
        raise ValueError('header must be exactly seven bytes')
    return (int.from_bytes(header[:2], 'big'),
            int.from_bytes(header[2:5], 'big'),
            int.from_bytes(header[5:], 'big'))


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info('peername')
    LOG.info('connection from %s', peer)
    try:
        while True:
            header = await asyncio.wait_for(reader.readexactly(HEADER_SIZE), 30)
            message_type, length, version = decode_header(header)
            if length > MAX_PAYLOAD:
                LOG.warning('invalid candidate frame size %s from %s', length, peer)
                break
            await asyncio.wait_for(reader.readexactly(length), 30)
            LOG.info('candidate frame type=%s bytes=%s version=%s from=%s',
                     message_type, length, version, peer)
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
    parser = argparse.ArgumentParser(description='Private Server v69 protocol probe')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=9339)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    server = await asyncio.start_server(handle_client, args.host, args.port)
    LOG.info('listening on %s; v69 framing and login are not yet verified',
             ', '.join(str(s.getsockname()) for s in server.sockets))
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
