import pathlib,zipfile,shutil
r=pathlib.Path('APK32');out=r/'online_test';out.mkdir(exist_ok=True)
with zipfile.ZipFile(r/'offline_test/base.apk') as zi,zipfile.ZipFile(out/'base.apk','w') as zo:
 for e in zi.infolist():
  if e.filename=='AndroidManifest.xml':
   d=zi.read(e);a='android.permission.INTERNEX'.encode('utf-16le');b='android.permission.INTERNET'.encode('utf-16le');assert d.count(a)==1;zo.writestr(e,d.replace(a,b))
  else:
   with zi.open(e) as x,zo.open(e,'w') as y:shutil.copyfileobj(x,y,1048576)
