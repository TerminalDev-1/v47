# Private Server — Brawl Stars v69

An early Python private-server project for Brawl Stars 69.414. **The client and server are not working together yet.** The 32-bit client starts loading game components but exits during protection checks. The server is a protocol probe, not a playable server.

## Test server

Requires Python 3.10 or newer. It listens only on the computer's loopback interface by default:

```powershell
python "Private Server/server.py"
adb reverse tcp:9339 tcp:9339
```

The USB forwarding makes the listener available to the tablet at `127.0.0.1:9339`; the client has not yet been patched to use it. The probe recognizes a candidate seven-byte frame from older versions, but v69 framing, encryption, login and gameplay remain unverified. It does not send responses. Run the tests with `python -m unittest discover -s tests -v`.

## APKs

The release includes the original 69.414 APKMirror bundle, which contains both ARM64 and ARM32 splits. It also contains a separate experimental 32-bit clone as five signed split APKs. The clone has package ID `com.supercell.brawlstarx` and requests INTERNET permission. It is incomplete and currently exits during startup; the original Supercell installation remains a separate package. Install the clone splits together, not the base alone.

The original and modified APK files are release assets because they exceed normal Git file-size limits. The release artifacts are snapshots; future source changes need new builds and releases. The local debug signing key is not published, so rebuilding with another key will not produce an update compatible with this installed clone without reinstalling it.

[Client investigation notes](APK32/INVESTIGATION.md) document the package-visibility fix, experiments, and remaining work. Reference APKs from other installed apps, generated files, logs and signing keys are excluded from Git. The small patch scripts reflect experimental work and depend on locally extracted files and Android tooling; they are not yet a complete portable build system.
