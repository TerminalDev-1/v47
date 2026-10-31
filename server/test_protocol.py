import asyncio,struct,unittest
from main import frame,read_frame,MAX_PAYLOAD
class FramingTests(unittest.IsolatedAsyncioTestCase):
 async def test_fragmented_and_consecutive_frames(self):
  reader=asyncio.StreamReader();wire=frame(10100,b'hello',1)+frame(10108)
  for b in wire:reader.feed_data(bytes([b]))
  self.assertEqual(await read_frame(reader),(10100,1,b'hello'))
  self.assertEqual(await read_frame(reader),(10108,0,b''))
 async def test_oversized_rejected_before_body(self):
  reader=asyncio.StreamReader();reader.feed_data(b'\x27\x74'+(MAX_PAYLOAD+1).to_bytes(3,'big')+b'\0\0')
  with self.assertRaises(ValueError):await read_frame(reader)
 async def test_truncated_frame(self):
  reader=asyncio.StreamReader();reader.feed_data(frame(10100,b'ab')[:-1]);reader.feed_eof()
  with self.assertRaises(asyncio.IncompleteReadError):await read_frame(reader)
if __name__=='__main__':unittest.main()
