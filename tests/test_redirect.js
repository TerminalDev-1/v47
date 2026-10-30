const assert = require('node:assert/strict');
const {loopbackForGamePort, GAME_PORT} = require('../client_patch/redirect.js');
function addr(family, port) {
  const b = new Uint8Array(family === 10 ? 28 : 16);
  b[0] = family; b[2] = port >> 8; b[3] = port & 255;
  b[4] = 203; b[5] = 0; b[6] = 113; b[7] = 3;
  return b;
}
for (const family of [2, 10]) {
  const original = addr(family, GAME_PORT);
  const redirected = loopbackForGamePort(original);
  assert.deepEqual(Array.from(redirected.slice(0, 8)), [2, 0, 0x24, 0x7b, 127, 0, 0, 1]);
  assert.equal(original[4], 203, 'original address must not be modified');
}
assert.equal(loopbackForGamePort(addr(2, 443)), null);
assert.equal(loopbackForGamePort(addr(1, GAME_PORT)), null);
assert.equal(loopbackForGamePort(new Uint8Array(3)), null);
console.log('redirect address tests passed');
