"""Local Brawl Stars 47.227 authenticated login and home-data service."""
import asyncio,datetime,json,pathlib,secrets,struct
from service import ServiceSession
from accounts import Accounts
from nacl.exceptions import CryptoError
from nacl.bindings import crypto_scalarmult_base
CAPTURES=pathlib.Path(__file__).resolve().parent/'captures'
MAX_PAYLOAD=4*1024*1024
DATA=pathlib.Path(__file__).resolve().parent/'data'
DATA.mkdir(exist_ok=True)
KEY_FILE=DATA/'server.key'
if not KEY_FILE.exists():
 with KEY_FILE.open('xb') as key_file:key_file.write(secrets.token_bytes(32))
PRIVATE_KEY=KEY_FILE.read_bytes()
ACCOUNTS=Accounts(DATA/'players.sqlite3')

def frame(message_id,payload=b'',version=0):
 if len(payload)>MAX_PAYLOAD:raise ValueError('oversized payload')
 return struct.pack('>H',message_id)+len(payload).to_bytes(3,'big')+struct.pack('>H',version)+payload

async def read_frame(reader):
 header=await reader.readexactly(7);size=int.from_bytes(header[2:5],'big')
 if size>MAX_PAYLOAD:raise ValueError('oversized frame')
 return int.from_bytes(header[:2],'big'),int.from_bytes(header[5:],'big'),await reader.readexactly(size)

async def client(reader,writer):
 CAPTURES.mkdir(exist_ok=True);tag=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f');sequence=0
 session=ServiceSession(PRIVATE_KEY,ACCOUNTS)
 print('CONNECTED',tag,flush=True)
 try:
  while True:
   mid,version,body=await read_frame(reader);sequence+=1
   (CAPTURES/f'{tag}-{sequence:04}-{mid}.bin').write_bytes(frame(mid,body,version))
   print(json.dumps({'connection':tag,'id':mid,'length':len(body),'version':version}),flush=True)
   responses=session.handle(mid,version,body)
   for response_id,response_version,response_payload in responses:
    writer.write(frame(response_id,response_payload,response_version))
    print('SENT',response_id,'bytes',len(response_payload),flush=True)
   await writer.drain()
 except asyncio.IncompleteReadError:print('DISCONNECTED',tag,flush=True)
 except (ValueError,ConnectionError,CryptoError) as e:print('CONNECTION ERROR',str(e),flush=True)
 finally:
  writer.close()
  try:await writer.wait_closed()
  except ConnectionError:pass

async def main():
 server=await asyncio.start_server(client,'127.0.0.1',19347)
 print('47.227 home-data service listening on 127.0.0.1:19347',flush=True)
 print('Client server public key:',crypto_scalarmult_base(PRIVATE_KEY).hex(),flush=True)
 async with server:await server.serve_forever()
if __name__=='__main__':asyncio.run(main())
