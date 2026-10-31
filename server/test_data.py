import tempfile,pathlib,unittest
from accounts import Accounts
from stream import Reader,Writer
class DataTests(unittest.TestCase):
 def test_signed_vint_boundaries_roundtrip(self):
  values=[-2147483648,-65,-64,-1,0,1,63,64,127,128,2147483647];w=Writer()
  for v in values:w.vint(v)
  r=Reader(w.bytes());self.assertEqual([r.vint() for _ in values],values)
 def test_boolean_groups_reset_on_non_boolean(self):
  w=Writer();w.boolean(True);w.boolean(False);w.boolean(True);w.vint(1);w.boolean(True)
  self.assertEqual(w.bytes(),b'\x05\x01\x01')
 def test_negative_and_excessive_string_lengths_rejected(self):
  for n in [-2,65537]:
   w=Writer();w.integer(n)
   with self.assertRaises(ValueError):Reader(w.bytes()).string()
 def test_account_persists_and_wrong_token_is_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   path=pathlib.Path(d)/'players.sqlite3';a=Accounts(path);p=a.login();b=Accounts(path)
   self.assertEqual(b.login(p['id'],p['token']),p)
   with self.assertRaises(ValueError):b.login(p['id'],'wrong')
