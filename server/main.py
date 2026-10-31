"""Brawl Stars 47.227 handshake server. Login crypto and home data are pending."""
import asyncio,datetime,json,pathlib,secrets,struct
CAPTURES=pathlib.Path(__file__).resolve().parent/'captures'
MAX_PAYLOAD=4*1024*1024

def frame(message_id,payload=b'',version=0):
 if len(payload)>MAX_PAYLOAD:raise ValueError('oversized payload')
 return struct.pack('>H',message_id)+len(payload).to_bytes(3,'big')+struct.pack('>H',version)+payload

async def read_frame(reader):
 header=await reader.readexactly(7);size=int.from_bytes(header[2:5],'big')
 if size>MAX_PAYLOAD:raise ValueError('oversized frame')
 return int.from_bytes(header[:2],'big'),int.from_bytes(header[5:],'big'),await reader.readexactly(size)

async def client(reader,writer):
 CAPTURES.mkdir(exist_ok=True);tag=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');sequence=0;hello=False
 print('CONNECTED',tag,flush=True)
 try:
  while True:
   mid,version,body=await read_frame(reader);sequence+=1
   (CAPTURES/f'{tag}-{sequence:04}-{mid}.bin').write_bytes(frame(mid,body,version))
   print(json.dumps({'connection':tag,'id':mid,'length':len(body),'version':version}),flush=True)
   if mid==10100:
    if hello:raise ValueError('duplicate ClientHello')
    hello=True;nonce=secrets.token_bytes(24)
    writer.write(frame(20100,struct.pack('>I',len(nonce))+nonce));await writer.drain()
    print('SENT ServerHello 20100',flush=True)
   elif mid==10108:
    writer.write(frame(20108));await writer.drain()
   elif mid==10101:
    print('LOGIN received; payload saved for crypto integration. No login success claimed.',flush=True)
   else:print('UNIMPLEMENTED',mid,flush=True)
 except asyncio.IncompleteReadError:print('DISCONNECTED',tag,flush=True)
 except (ValueError,ConnectionError) as e:print('CONNECTION ERROR',str(e),flush=True)
 finally:
  writer.close()
  try:await writer.wait_closed()
  except ConnectionError:pass

async def main():
 server=await asyncio.start_server(client,'127.0.0.1',19347)
 print('47.227 handshake server listening on 127.0.0.1:19347',flush=True)
 async with server:await server.serve_forever()
if __name__=='__main__':asyncio.run(main())
