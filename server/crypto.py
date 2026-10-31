"""Authenticated Pepper transport used by the v47 client handshake."""
import hashlib,secrets
from nacl.bindings import crypto_box_beforenm,crypto_secretbox,crypto_secretbox_open,crypto_scalarmult_base
from nacl.exceptions import CryptoError

def nonce_hash(*parts):return hashlib.blake2b(b''.join(parts),digest_size=24).digest()
def increment(nonce):return ((int.from_bytes(nonce,'little')+2)%(1<<192)).to_bytes(24,'little')

class PepperSession:
 def __init__(self,private_key,session_token):
  if len(private_key)!=32 or len(session_token)!=24:raise ValueError('Invalid key or session token length')
  self.private_key=private_key;self.public_key=crypto_scalarmult_base(private_key);self.token=session_token
  self.client_public=None;self.client_nonce=None;self.server_nonce=None;self.key=None;self.established=False
 def decrypt_login(self,payload):
  if self.client_public is not None:raise ValueError('Duplicate login')
  if len(payload)<32+16+48:raise ValueError('Truncated encrypted login')
  public=payload[:32];key=crypto_box_beforenm(public,self.private_key)
  plain=crypto_secretbox_open(payload[32:],nonce_hash(public,self.public_key),key)
  if not secrets.compare_digest(plain[:24],self.token):raise ValueError('Login session token mismatch')
  self.client_public=public;self.client_nonce=plain[24:48];self.key=key
  return plain[48:]
 def encrypt_login_response(self,payload):
  if self.client_nonce is None or self.established:raise ValueError('Login response out of sequence')
  server_nonce=secrets.token_bytes(24);session_key=secrets.token_bytes(32)
  result=crypto_secretbox(server_nonce+session_key+payload,nonce_hash(self.client_nonce,self.client_public,self.public_key),self.key)
  self.server_nonce=server_nonce;self.key=session_key;self.established=True
  return result
 def encrypt(self,payload):
  if not self.established:raise ValueError('Session not established')
  nonce=increment(self.server_nonce);result=crypto_secretbox(payload,nonce,self.key);self.server_nonce=nonce;return result
 def decrypt(self,payload):
  if not self.established:raise ValueError('Session not established')
  nonce=increment(self.client_nonce);result=crypto_secretbox_open(payload,nonce,self.key);self.client_nonce=nonce;return result
