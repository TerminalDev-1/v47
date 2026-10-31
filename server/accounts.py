import pathlib,secrets,sqlite3,time
from contextlib import contextmanager
class Accounts:
 def __init__(self,path):
  self.path=pathlib.Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.connect() as db:db.execute('CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, token TEXT UNIQUE NOT NULL, name TEXT NOT NULL, created INTEGER NOT NULL)')
 @contextmanager
 def connect(self):
  db=sqlite3.connect(self.path)
  try:
   with db:yield db
  finally:db.close()
 def login(self,account_id=0,token=None):
  with self.connect() as db:
   if account_id:
    row=db.execute('SELECT id, token, name FROM players WHERE id=?',(account_id,)).fetchone()
    if row is None or not token or not secrets.compare_digest(row[1],token):raise ValueError('Invalid account credentials')
   else:
    new_token=secrets.token_urlsafe(32);cur=db.execute('INSERT INTO players(token,name,created) VALUES(?,?,?)',(new_token,'Player',int(time.time())))
    row=(cur.lastrowid,new_token,'Player')
  return {'id':row[0],'token':row[1],'name':row[2]}
