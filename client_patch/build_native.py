"""Package a version-specific ARM32 native bootstrap and redirect experiment."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
APK32 = ROOT / 'APK32'
OUT = ROOT / 'build' / 'native'
EXPECTED_LIBRARIES = {
    'lib/armeabi-v7a/libg.so': '552d1880290cec5406b0d4bd8bd5f887a48739b100766e247a57b3e60b4471f2',
    'lib/armeabi-v7a/libsupercell_brawlstars.so': 'a01421fd1faef4223a171ce01e9eb26b6825a4f96664747dd5b6e6ec5d67e1a2',
}
ORIGINAL_BASE_HASH = '4e83a342a854f24fd44e67f3231a560e6aac775df77dffb58503f245d4677554'
DEVICE_FILES = '/sdcard/Android/data/com.supercell.brawlstarx/files'


def run(*args):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    sources = [APK32 / 'online_test/base.apk', APK32 / 'unsigned/split_config.armeabi_v7a.apk',
               APK32 / 'native-dex-source.apk', ROOT / 'client_patch/libpshook.so',
               ROOT / 'tools/uber-apk-signer.jar']
    missing = [str(p) for p in sources if not p.is_file()]
    if missing:
        raise SystemExit('Missing prepared inputs:\n' + '\n'.join(missing))
    original_base = APK32 / 'original/base.apk'
    if args.install:
        if not original_base.is_file() or hashlib.sha256(original_base.read_bytes()).hexdigest() != ORIGINAL_BASE_HASH:
            raise SystemExit('Missing or unexpected original 69.414 base APK; refusing install')
    with zipfile.ZipFile(sources[1]) as abi:
        for name, expected in EXPECTED_LIBRARIES.items():
            if hashlib.sha256(abi.read(name)).hexdigest() != expected:
                raise SystemExit(f'Unexpected library {name}: refusing version-specific patch')
    unsigned = OUT / 'unsigned'
    signed = OUT / 'signed'
    unsigned.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(sources[2]) as dex:
        for index, name in enumerate(('base.apk', 'split_config.armeabi_v7a.apk')):
            with zipfile.ZipFile(sources[index]) as source, zipfile.ZipFile(unsigned / name, 'w') as out:
                for entry in source.infolist():
                    if index == 0 and entry.filename in ('classes.dex', 'classes2.dex'):
                        out.writestr(entry, dex.read(entry.filename))
                    else:
                        with source.open(entry) as src, out.open(entry, 'w') as dst:
                            shutil.copyfileobj(src, dst, 1024 * 1024)
                if index == 1:
                    out.write(sources[3], 'lib/armeabi-v7a/libpshook.so', compress_type=zipfile.ZIP_DEFLATED)
    run('java', '-jar', sources[4], '-a', unsigned, '-o', signed)
    if args.install:
        files = sorted(signed.glob('*-aligned-debugSigned.apk'))
        if len(files) != 2:
            raise SystemExit('Expected precisely two signed splits')
        run('adb', '-d', 'shell', 'am', 'force-stop', 'com.supercell.brawlstarx')
        run('adb', '-d', 'install-multiple', '-r', '-p', 'com.supercell.brawlstarx', *files)
        run('adb', '-d', 'shell', 'mkdir', '-p', DEVICE_FILES)
        run('adb', '-d', 'push', original_base, DEVICE_FILES + '/original_base.apk')
        run('adb', '-d', 'reverse', 'tcp:9339', 'tcp:9339')


if __name__ == '__main__':
    main()
