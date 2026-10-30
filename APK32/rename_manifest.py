import zipfile,pathlib,shutil
root=pathlib.Path(__file__).resolve().parent
src=root/'original'; dst=root/'unsigned'; dst.mkdir(exist_ok=True)
old='com.supercell.brawlstars'.encode('utf-16le'); new='com.supercell.brawlstarx'.encode('utf-16le')
for f in src.glob('*.apk'):
 print('Processing',f.name,flush=True)
 with zipfile.ZipFile(f) as zi, zipfile.ZipFile(dst/f.name,'w',allowZip64=True) as zo:
  for entry in zi.infolist():
   if entry.filename.upper().startswith('META-INF/') and (entry.filename.upper().endswith(('.SF','.RSA','.DSA','.EC')) or entry.filename.upper() == 'META-INF/MANIFEST.MF'): continue
   if entry.filename=='AndroidManifest.xml':
    data=zi.read(entry); count=data.count(old); data=data.replace(old,new).replace(new+'.GameApp'.encode('utf-16le'),old+'.GameApp'.encode('utf-16le')); print('  Manifest replacements:',count,flush=True)
    if not count: raise ValueError('Package string missing')
    zo.writestr(entry,data)
   else:
    with zi.open(entry) as inp, zo.open(entry,'w',force_zip64=entry.file_size>0x7fffffff) as out: shutil.copyfileobj(inp,out,1024*1024)
