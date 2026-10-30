# Private Server — Brawl Stars v69

Private Server is a Python private server for Brawl Stars 69.414. It is in **very early development**: the client and server do not work together yet, and login and gameplay have not been implemented.

## Current development status

The Python server implements the initial ClientHello (10100) and ServerHello (20100) exchange. An independent v69-format reference client completed this exchange; the actual 69.414 Android client has not yet connected. The 32-bit client copy exits during startup despite experimental native redirect and bootstrap changes. Login, encryption, and gameplay remain unimplemented.

Requires Python 3.10 or newer. To start the test listener and forward the port over USB:

```powershell
python "Private Server/server.py"
adb -d reverse tcp:9339 tcp:9339
```

The listener binds to `127.0.0.1:9339` by default. It reads seven-byte frames and responds to a valid ClientHello with a 24-byte ServerHello challenge. The initial message layout was checked against the [laserjs v69 reference client](https://github.com/justflyne/laserjs); it still needs verification with this Android build. Run its tests with `python -m unittest discover -s tests -v`.

## APKs

The release contains the original 69.414 APKMirror bundle with ARM64 and ARM32 splits, plus five signed split APKs for a separate 32-bit client copy. The copy uses package ID `com.supercell.brawlstarx` and requests INTERNET permission. It currently exits during startup and is not playable. Install all five splits together; the official Supercell game remains a separate package.

The APKs are versioned release assets. The local debug signing key is not published, so a rebuild signed with a different key requires reinstalling the client copy.

[Client development notes](APK32/DEVELOPMENT.md) record completed work and remaining issues. Generated files, logs, reference APKs from other apps and signing keys are excluded from Git. The included patch scripts are experimental and do not yet form a complete portable build system.

## USB redirect development

The experimental redirect is in `client_patch/redirect.js`. It matches port 9339; the actual Android client's destination remains unverified. Build with `python client_patch/build_redirect.py --install` using the prepared local APK, decoded dex and signing tools. The command targets the USB device with `adb -d`. The optional `--self-test` sends a synthetic frame to validate the redirect; it is not a game login. Run `node tests/test_redirect.js` for address-rewrite tests. A separate experimental ARM32 native bootstrap is in `client_patch/native_redirect.c`; it is tied to the exact 69.414 libraries and has not resolved the startup failure.
