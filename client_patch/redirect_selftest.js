// Controlled test: this is not a game connection.
Interceptor.flush();
const sock = new NativeFunction(Module.getGlobalExportByName('socket'), 'int', ['int', 'int', 'int']);
const connectTest = new NativeFunction(Module.getGlobalExportByName('connect'), 'int', ['int', 'pointer', 'int'], { traps: 'all' });
const writeTest = new NativeFunction(Module.getGlobalExportByName('write'), 'int', ['int', 'pointer', 'int']);
const closeTest = new NativeFunction(Module.getGlobalExportByName('close'), 'int', ['int']);
const testLog = new NativeFunction(Module.getGlobalExportByName('__android_log_write'), 'int', ['int','pointer','pointer']);
const fdTest = sock(2, 1, 0);
const addrTest = Memory.alloc(16);
addrTest.writeByteArray([2,0,0x24,0x7b,198,51,100,1,0,0,0,0,0,0,0,0]);
const resultTest = connectTest(fdTest, addrTest, 16);
testLog(4, Memory.allocUtf8String('PrivateServer'), Memory.allocUtf8String('controlled socket test result=' + resultTest));
if (resultTest === 0) {
  const frame = Memory.alloc(7);
  frame.writeByteArray([0x27,0x74,0,0,0,0,1]);
  const written = writeTest(fdTest, frame, 7);
  testLog(4, Memory.allocUtf8String('PrivateServer'), Memory.allocUtf8String('controlled test bytes=' + written));
  new NativeFunction(Module.getGlobalExportByName('usleep'), 'int', ['uint'])(500000);
}
closeTest(fdTest);
