/* Redirect the candidate game TCP port through adb reverse. */
'use strict';
const GAME_PORT = 9339;

// Android sockaddr_in and sockaddr_in6 use a native-endian family and a
// network-endian port. The returned IPv4 sockaddr works with adb reverse.
function loopbackForGamePort(bytes) {
  if (bytes.length < 8) return null;
  const family = bytes[0] | (bytes[1] << 8);
  const port = (bytes[2] << 8) | bytes[3];
  if ((family !== 2 && family !== 10) || port !== GAME_PORT) return null;
  const result = new Uint8Array(16);
  result[0] = 2;
  result[2] = (GAME_PORT >> 8) & 255;
  result[3] = GAME_PORT & 255;
  result.set([127, 0, 0, 1], 4);
  return result;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { loopbackForGamePort, GAME_PORT };
}

if (typeof Interceptor !== 'undefined') {
  const logFn = new NativeFunction(Module.getGlobalExportByName('__android_log_write'), 'int', ['int', 'pointer', 'pointer']);
  function log(s) { logFn(4, Memory.allocUtf8String('PrivateServer'), Memory.allocUtf8String(s)); }
  const connect = Module.getGlobalExportByName('connect');
  Interceptor.attach(connect, {
    onEnter(args) {
      if (args[1].isNull() || args[2].toInt32() < 8) return;
      try {
        const bytes = new Uint8Array(args[1].readByteArray(Math.min(args[2].toInt32(), 28)));
        const target = loopbackForGamePort(bytes);
        if (target === null) return;
        this.target = Memory.alloc(target.length);
        this.target.writeByteArray(target);
        args[1] = this.target;
        args[2] = ptr(target.length);
        log('redirected candidate game port to 127.0.0.1:9339');
      } catch (e) { log('redirect error: ' + e); }
    }
  });
  log('redirect hook installed; game port is unverified for v69');
}
