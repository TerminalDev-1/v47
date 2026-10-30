import asyncio
import importlib.util
import pathlib
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
                writer.write(bytes.fromhex('277400'))
                await writer.drain()
                await asyncio.sleep(0.02)
                writer.write(bytes.fromhex('00030001') + b'abc')
                await writer.drain()
                await asyncio.sleep(0.05)
                writer.close()
                await writer.wait_closed()
                await asyncio.sleep(0.05)
            self.assertTrue(any('type=10100 bytes=3 version=1' in line for line in logs.output))
        finally:
            listener.close()
            await listener.wait_closed()

if __name__ == '__main__':
    unittest.main()
