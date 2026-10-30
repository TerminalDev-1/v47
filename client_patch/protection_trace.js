// Experimental test: suppress the identified protection shutdown worker.
const shutdownLog = new NativeFunction(Module.getGlobalExportByName('__android_log_write'), 'int', ['int','pointer','pointer']);
function protectLog(s) { shutdownLog(4, Memory.allocUtf8String('PrivateServerTrace'), Memory.allocUtf8String(s)); }
const harmlessWorker = new NativeCallback(function (_) { return ptr(0); }, 'pointer', ['pointer']);
Interceptor.attach(Module.getGlobalExportByName('pthread_create'), {
  onEnter(args) {
    const start = args[2];
    const module = Process.findModuleByAddress(start.and(ptr('0xfffffffe')));
    if (!module || module.name !== 'libsupercell_brawlstars.so') return;
    const offset = start.sub(module.base).toUInt32() & 0xfffffffe;
    if (offset === 0x34bb34) { args[2] = harmlessWorker; protectLog('suppressed shutdown worker'); }
  }
});
protectLog('startup worker filter active');
for (const name of ['exit','_exit','_Exit','abort','kill','killpg','raise']) {
 const f = Module.findGlobalExportByName(name); if (!f) continue;
 try { Interceptor.attach(f, {onEnter(args) {
   const mod=Process.findModuleByAddress(this.returnAddress);
   protectLog(name+' arg0='+args[0]+' from='+(mod?mod.name+'+'+this.returnAddress.sub(mod.base):this.returnAddress)); if(name==='abort'&&mod&&mod.name==='libsupercell_brawlstars.so'){let a=mod.base.add(0x1f8560);protectLog('ABORTCODE '+Array.from(new Uint8Array(a.readByteArray(112))).map(x=>x.toString(16).padStart(2,'0')).join(''));}
 }}); } catch(e) { protectLog('hook '+name+' '+e); }
}
