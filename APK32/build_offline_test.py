import zipfile,pathlib,shutil
r=pathlib.Path('APK32'); d=r/'offline_test';d.mkdir(exist_ok=True)
with zipfile.ZipFile(r/'query_fixed/base.apk') as zi, zipfile.ZipFile(r/'instrumentation-source.apk') as dex,zipfile.ZipFile(d/'base.apk','w') as zo:
 for e in zi.infolist():
  if e.filename=='AndroidManifest.xml':
   data=zi.read(e);a='android.permission.INTERNET'.encode('utf-16le');b='android.permission.INTERNEX'.encode('utf-16le');assert data.count(a)==1;zo.writestr(e,data.replace(a,b))
  elif e.filename in ('classes.dex','classes2.dex'):zo.writestr(e,dex.read(e.filename))
  else:
   with zi.open(e) as x,zo.open(e,'w') as y:shutil.copyfileobj(x,y,1048576)
