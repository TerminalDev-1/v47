"""Build the experimental USB redirect splits from prepared local inputs."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APK32 = ROOT / 'APK32'
OUT = ROOT / 'build' / 'redirect'
UNSIGNED = OUT / 'unsigned'
SIGNED = OUT / 'signed'


def run(*args):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protection-trace', action='store_true', help='build a temporary startup diagnostic')
    parser.add_argument('--self-test', action='store_true', help='send a controlled test frame before startup')
    parser.add_argument('--install', action='store_true', help='update the clone using the USB-connected device')
    args = parser.parse_args()
    inputs = [APK32 / 'online_test/base.apk', APK32 / 'unsigned/split_config.armeabi_v7a.apk',
              APK32 / 'instrumentation-source.apk', ROOT / 'tools/libfrida-gadget-arm.so',
              ROOT / 'tools/uber-apk-signer.jar']
    missing = [str(p) for p in inputs if not p.is_file()]
    if missing:
        raise SystemExit('Missing prepared inputs:\n' + '\n'.join(missing))
    UNSIGNED.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(inputs[2]) as dex:
        if b'gadget' not in dex.read('classes.dex'):
            raise SystemExit('Prepared dex does not contain the gadget loader; rebuild the instrumented dex first')
        for index, name in enumerate(('base.apk', 'split_config.armeabi_v7a.apk')):
            with zipfile.ZipFile(inputs[index]) as source, zipfile.ZipFile(UNSIGNED / name, 'w') as out:
                for entry in source.infolist():
                    if name == 'base.apk' and entry.filename in ('classes.dex', 'classes2.dex'):
                        out.writestr(entry, dex.read(entry.filename))
                    else:
                        with source.open(entry) as src, out.open(entry, 'w') as dst:
                            shutil.copyfileobj(src, dst, 1024 * 1024)
                if index == 1:
                    directory = 'lib/armeabi-v7a/'
                    out.write(inputs[3], directory + 'libgadget.so', compress_type=zipfile.ZIP_DEFLATED)
                    out.writestr(directory + 'libgadget.config.so', json.dumps({'interaction': {'type': 'script', 'path': 'libgadget.script.so'}}))
                    script = (ROOT / 'client_patch/redirect.js').read_text(encoding='utf-8')
                    if args.protection_trace:
                        script += '\n' + (ROOT / 'client_patch/protection_trace.js').read_text(encoding='utf-8')
                    if args.self_test:
                        script += '\n' + (ROOT / 'client_patch/redirect_selftest.js').read_text(encoding='utf-8')
                    out.writestr(directory + 'libgadget.script.so', script)
    run('java', '-jar', inputs[4], '-a', UNSIGNED, '-o', SIGNED)
    if args.install:
        files = sorted(SIGNED.glob('*-aligned-debugSigned.apk'))
        if len(files) != 2:
            raise SystemExit('Expected precisely two signed APK splits')
        run('adb', '-d', 'shell', 'am', 'force-stop', 'com.supercell.brawlstarx')
        run('adb', '-d', 'install-multiple', '-r', '-p', 'com.supercell.brawlstarx', *files)
        run('adb', '-d', 'reverse', 'tcp:9339', 'tcp:9339')


if __name__ == '__main__':
    main()
