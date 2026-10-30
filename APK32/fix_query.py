"""Restore the original package visibility query in the cloned binary manifest."""
import struct,zipfile,pathlib,shutil
root=pathlib.Path(__file__).resolve().parent
src=root/'unsigned'/'base.apk'; out=root/'query_fixed'; out.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z: b=bytearray(z.read('AndroidManifest.xml'))
u16=lambda p:struct.unpack_from('<H',b,p)[0]
u32=lambda p:struct.unpack_from('<I',b,p)[0]
assert u16(8)==1 and u32(24)==0
pool_size=u32(12); count=u32(16); start=u32(28); style_count=u32(20); assert style_count==0
old=b[8:8+pool_size]; offsets=old[28:28+count*4]; data=bytes(old[start:]).rstrip(b'\0')
# Preserve UTF-16 terminators and alignment exactly; append after the original pool data.
data=bytes(old[start:]); name='com.supercell.brawlstars'; new=struct.pack('<H',len(name))+name.encode('utf-16le')+b'\0\0'; pos=len(data); data+=new; data+=b'\0'*((-len(data))%4)
header=bytearray(old[:28]); new_start=start+4; struct.pack_into('<I',header,4,28+len(offsets)+4+len(data));struct.pack_into('<I',header,8,count+1);struct.pack_into('<I',header,20,new_start)
pool=header+offsets+struct.pack('<I',pos)+data
b=bytearray(b[:8]+pool+b[8+pool_size:]);struct.pack_into('<I',b,4,len(b))
# The first <package android:name=...> is the visibility query for the game.
o=8+len(pool); done=False
while o<len(b):
 typ=struct.unpack_from('<H',b,o)[0]; size=struct.unpack_from('<I',b,o+4)[0]
 if typ==0x102:
  nameidx=struct.unpack_from('<I',b,o+20)[0]
  # Element name resolved through the unchanged original pool.
  npos=8+new_start+struct.unpack_from('<I',b,8+28+nameidx*4)[0]
  nlen=struct.unpack_from('<H',b,npos)[0]; elem=b[npos+2:npos+2+nlen*2].decode('utf-16le')
  if elem=='package':
   astart=struct.unpack_from('<H',b,o+24)[0]; attr=o+16+astart
   struct.pack_into('<I',b,attr+8,count);struct.pack_into('<I',b,attr+16,count);done=True;break
 o+=size
assert done
with zipfile.ZipFile(src) as zi,zipfile.ZipFile(out/'base.apk','w',allowZip64=True) as zo:
 for e in zi.infolist():
  if e.filename=='AndroidManifest.xml':zo.writestr(e,b)
  else:
   with zi.open(e) as a,zo.open(e,'w') as c:shutil.copyfileobj(a,c,1048576)
print('Wrote',out/'base.apk')
