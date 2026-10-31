from types import SimpleNamespace
from stream import Reader
from schemas.loginok import LoginOk
from schemas.ownhomedata import OwnHomeData

def parse_login(payload):
 r=Reader(payload);account_id=r.long();token=r.string();major=r.integer();minor=r.integer();build=r.integer();fingerprint=r.string()
 if major!=47 or build!=227:raise ValueError('Expected client 47.227')
 return account_id,token,{'major':major,'minor':minor,'build':build,'fingerprint':fingerprint}

def player_view(account):
 return SimpleNamespace(ID=[0,account['id']],Token=account['token'],Name=account['name'],Registered=True,Trophies=0,HighestTrophies=0,TrophyRoadTier=0,Thumbnail=0,Namecolor=0,Coins=1000,Gems=100,StarPoints=0,SelectedBrawlers=[0,0,0],OwnedPins=[],OwnedThumbnails=[0],OwnedBrawlers={0:{'CardID':0,'Skins':[],'Trophies':0,'HighestTrophies':0,'PowerLevel':1,'PowerPoints':0,'State':2}})

def login_ok(account):
 writer=LoginOk();writer.encode({},player_view(account));return writer.bytes()
def own_home_data(account):
 writer=OwnHomeData();writer.encode({},player_view(account));return writer.bytes()
