import unittest,secrets,tempfile,pathlib,struct
from accounts import Accounts
from service import ServiceSession
from stream import Writer,Reader
from crypto import nonce_hash,increment
from nacl.bindings import crypto_scalarmult_base,crypto_box_beforenm,crypto_secretbox,crypto_secretbox_open
class ServiceTests(unittest.TestCase):
 def test_login_returns_authenticated_loginok_and_home(self):
  with tempfile.TemporaryDirectory() as d:
   key=secrets.token_bytes(32);session=ServiceSession(key,Accounts(pathlib.Path(d)/'players.sqlite3'))
   hello=session.handle(10100,0,struct.pack('>5I',2,35,47,0,227))[0];token=hello[2][4:]
   private=secrets.token_bytes(32);public=crypto_scalarmult_base(private);server=crypto_scalarmult_base(key);shared=crypto_box_beforenm(server,private);nonce=secrets.token_bytes(24)
   w=Writer();w.long(0);w.string();w.integer(47);w.integer(0);w.integer(227);w.string('test-fingerprint')
   login=public+crypto_secretbox(token+nonce+w.bytes(),nonce_hash(public,server),shared)
   result=session.handle(10101,10,login);self.assertEqual([(m,v) for m,v,b in result],[(20104,1),(24101,0)])
   first=crypto_secretbox_open(result[0][2],nonce_hash(nonce,public,server),shared);server_nonce,transport_key,body=first[:24],first[24:56],first[56:]
   self.assertEqual(Reader(body).long(),session.account['id'])
   home=crypto_secretbox_open(result[1][2],increment(server_nonce),transport_key);self.assertIn(b'Player',home);self.assertGreater(len(home),500)
   beat=crypto_secretbox(b'',increment(nonce),transport_key);reply=session.handle(10108,0,beat)[0]
   self.assertEqual(reply[0],20108);self.assertEqual(crypto_secretbox_open(reply[2],increment(increment(server_nonce)),transport_key),b'')
 def test_login_before_hello_is_rejected(self):
  session=ServiceSession(secrets.token_bytes(32),None)
  with self.assertRaises(ValueError):session.handle(10101,10,b'bad')
