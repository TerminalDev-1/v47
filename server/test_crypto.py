import unittest,secrets
from nacl.bindings import crypto_scalarmult_base,crypto_box_beforenm,crypto_secretbox,crypto_secretbox_open
from nacl.exceptions import CryptoError
from crypto import PepperSession,nonce_hash,increment
class CryptoTests(unittest.TestCase):
 def setUp(self):
  self.token=secrets.token_bytes(24);self.session=PepperSession(secrets.token_bytes(32),self.token)
  self.client_private=secrets.token_bytes(32);self.client_public=crypto_scalarmult_base(self.client_private)
  self.shared=crypto_box_beforenm(self.session.public_key,self.client_private);self.nonce=secrets.token_bytes(24)
 def login(self,token=None):return self.client_public+crypto_secretbox((token or self.token)+self.nonce+b'login payload',nonce_hash(self.client_public,self.session.public_key),self.shared)
 def test_full_authenticated_handshake_and_bidirectional_transport(self):
  self.assertEqual(self.session.decrypt_login(self.login()),b'login payload')
  box=self.session.encrypt_login_response(b'login ok');plain=crypto_secretbox_open(box,nonce_hash(self.nonce,self.client_public,self.session.public_key),self.shared)
  nonce,key,body=plain[:24],plain[24:56],plain[56:];self.assertEqual(body,b'login ok')
  home=self.session.encrypt(b'home payload');self.assertEqual(crypto_secretbox_open(home,increment(nonce),key),b'home payload')
  msg=crypto_secretbox(b'keepalive',increment(self.nonce),key);self.assertEqual(self.session.decrypt(msg),b'keepalive')
 def test_wrong_token_rejected(self):
  with self.assertRaises(ValueError):self.session.decrypt_login(self.login(secrets.token_bytes(24)))
 def test_modified_ciphertext_rejected(self):
  data=bytearray(self.login());data[-1]^=1
  with self.assertRaises(CryptoError):self.session.decrypt_login(bytes(data))
 def test_nonce_not_advanced_on_authentication_failure(self):
  self.session.decrypt_login(self.login());self.session.encrypt_login_response(b'ok');before=self.session.client_nonce
  with self.assertRaises(CryptoError):self.session.decrypt(b'bad')
  self.assertEqual(self.session.client_nonce,before)
