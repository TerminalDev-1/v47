"""Connection state machine: hello, authenticated login, then home data."""
import secrets,struct
from crypto import PepperSession
from messages import parse_login,login_ok,own_home_data
from stream import Reader
class ServiceSession:
 def __init__(self,private_key,accounts):self.private_key=private_key;self.accounts=accounts;self.crypto=None;self.account=None
 def handle(self,mid,version,payload):
  if mid==10100:
   if self.crypto is not None:raise ValueError('Duplicate hello')
   r=Reader(payload);protocol,key_version,major,minor,build=[r.integer() for _ in range(5)]
   if (protocol,key_version,major,build)!=(2,35,47,227):raise ValueError('Unsupported client handshake')
   nonce=secrets.token_bytes(24);self.crypto=PepperSession(self.private_key,nonce)
   return [(20100,0,struct.pack('>I',24)+nonce)]
  if self.crypto is None:raise ValueError('Hello required')
  if mid==10101:
   if self.account is not None:raise ValueError('Duplicate login')
   plain=self.crypto.decrypt_login(payload);account_id,token,version_info=parse_login(plain)
   self.account=self.accounts.login(account_id,token)
   ok=self.crypto.encrypt_login_response(login_ok(self.account));home=self.crypto.encrypt(own_home_data(self.account))
   return [(20104,1,ok),(24101,0,home)]
  if self.account is None:raise ValueError('Login required')
  plain=self.crypto.decrypt(payload)
  if mid==10108:return [(20108,0,self.crypto.encrypt(b''))]
  if mid in (14101,14109,14102):return [(24101,0,self.crypto.encrypt(own_home_data(self.account)))]
  return []
