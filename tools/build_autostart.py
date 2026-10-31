import pathlib,zipfile,copy,json
root=pathlib.Path('build/instrumentation')
js=pathlib.Path('tools/startup.js').read_text()
(root/'startup.js').write_text(js)
config={'interaction':{'type':'script','path':'libstartup.so','on_change':'ignore'}}
with zipfile.ZipFile(root/'tablet-diagnostic.apk') as zi,zipfile.ZipFile(root/'tablet-autostart.apk','w') as zo:
 for info in zi.infolist():zo.writestr(copy.copy(info),zi.read(info))
 zo.writestr('lib/arm64-v8a/libdiagnostic.config.so',json.dumps(config),compress_type=zipfile.ZIP_DEFLATED)
 zo.writestr('lib/arm64-v8a/libstartup.so',js,compress_type=zipfile.ZIP_DEFLATED)
print('Bundled automatic startup fix; no controller connection required')
