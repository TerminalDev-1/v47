import subprocess,struct,sys,threading
sys.path.insert(0,'server');from main import frame
hello=frame(10100,struct.pack('>7I',3,0,47,227,1,0,0))
proc=subprocess.Popen(['adb','-s','f298358c','shell','toybox','nc','-w','5','127.0.0.1','19347'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
timer=threading.Timer(7,proc.kill);timer.start()
try:
 proc.stdin.write(hello);proc.stdin.flush();b=proc.stdout.read(35)
finally:
 timer.cancel();proc.terminate();proc.wait(timeout=3)
print('Tablet USB tunnel response bytes:',len(b))
assert len(b)>=7,'No response received over tablet tunnel'
assert int.from_bytes(b[:2],'big')==20100,'Expected ServerHello'
size=int.from_bytes(b[2:5],'big');assert size==28 and len(b)==35
assert int.from_bytes(b[7:11],'big')==24
print('PASS: ServerHello 20100 received through the physical tablet USB tunnel')
