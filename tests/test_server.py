import asyncio
import importlib.util
import pathlib
import struct
import unittest

path = pathlib.Path(__file__).resolve().parents[1] / 'Private Server' / 'server.py'
spec = importlib.util.spec_from_file_location('private_server', path)
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class ProtocolProbeTests(unittest.IsolatedAsyncioTestCase):
    def test_header(self):
        self.assertEqual(server.decode_header(bytes.fromhex('27740000030001')), (10100, 3, 1))
        with self.assertRaises(ValueError):
            server.decode_header(b'bad')

    async def test_fragmented_frame_and_disconnect(self):
        listener = await asyncio.start_server(server.handle_client, '127.0.0.1', 0)
        try:
            reader, writer = await asyncio.open_connection(*listener.sockets[0].getsockname())
            with self.assertLogs('private_server', level='INFO') as logs:
                fingerprint = b'abc123'
                payload = struct.pack('>6i', 2, 59, 69, 1, 414, len(fingerprint)) + fingerprint + struct.pack('>2i', 2, 2)
                frame = server.encode_frame(10100, payload)
                writer.write(frame[:3])
                await writer.drain()
                await asyncio.sleep(0.02)
                writer.write(frame[3:])
                await writer.drain()
                header = await asyncio.wait_for(reader.readexactly(7), 1)
                kind, size, version = server.decode_header(header)
                self.assertEqual((kind, size, version), (20100, 28, 0))
                body = await asyncio.wait_for(reader.readexactly(size), 1)
                self.assertEqual(struct.unpack_from('>i', body)[0], 24)
                writer.close()
                await writer.wait_closed()
                await asyncio.sleep(0.05)
            self.assertTrue(any('ClientHello client=69.414 build=1' in line for line in logs.output))
            self.assertTrue(any('ServerHello sent' in line for line in logs.output))
        finally:
            listener.close()
            await listener.wait_closed()

    async def test_malformed_hello_closes_without_reply(self):
        listener = await asyncio.start_server(server.handle_client, '127.0.0.1', 0)
        try:
            reader, writer = await asyncio.open_connection(*listener.sockets[0].getsockname())
            writer.write(server.encode_frame(10100, b'bad'))
            await writer.drain()
            self.assertEqual(await asyncio.wait_for(reader.read(), 1), b'')
            writer.close()
            await writer.wait_closed()
        finally:
            listener.close()
            await listener.wait_closed()

if __name__ == '__main__':
    unittest.main()
