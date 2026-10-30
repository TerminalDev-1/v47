import struct,zipfile
z=zipfile.ZipFile('APK32/unsigned/base.apk'); b=z.read('AndroidManifest.xml'); u16=lambda i:struct.unpack_from('<H',b,i)[0];u32=lambda i:struct.unpack_from('<I',b,i)[0];o=8;assert u16(o)==1
sz=u32(o+4); count=u32(o+8); flags=u32(o+16); start=u32(o+20);print('pool',sz,count,hex(flags),start)
strings=[]
for i in range(count):
 pos=o+start+u32(o+28+i*4); n=u16(pos); strings.append(b[pos+2:pos+2+n*2].decode('utf-16le'))
o+=sz
while o<len(b):
 typ=u16(o); size=u32(o+4)
 if typ==0x102:
  name=strings[u32(o+20)]; astart=u16(o+24); asize=u16(o+26); acount=u16(o+28)
  if name in ('manifest','queries','package'):
   print('element',name,'offset',o,'attrs',acount)
   for j in range(acount):
    p=o+16+astart+j*asize; ns,nam,raw,typed=struct.unpack_from('<IIII',b,p); data=u32(p+16)
    print('  ',strings[nam],strings[raw] if raw< len(strings) else raw,'value',strings[data] if data<len(strings) else data,'at',p)
 if not size:break
 o+=size
