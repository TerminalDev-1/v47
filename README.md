# Private Server — Brawl Stars v69

Private Server is a Python private server for Brawl Stars 69.414. It is in **very early development**: the client and server do not work together yet, and login and gameplay have not been implemented.

## Current development status

The server is a test listener for exploring the protocol. The 32-bit client copy loads game components but exits during startup. Its server address still needs to be redirected to the private server, and the v69 message format and encryption need to be implemented.

Requires Python 3.10 or newer. To start the test listener and forward the port over USB:

```powershell
python "Private Server/server.py"
adb reverse tcp:9339 tcp:9339
```

The listener binds to `127.0.0.1:9339` by default. It currently reads a candidate seven-byte frame based on an older version and does not send responses. Run its tests with `python -m unittest discover -s tests -v`.

## APKs

The release contains the original 69.414 APKMirror bundle with ARM64 and ARM32 splits, plus five signed split APKs for a separate 32-bit client copy. The copy uses package ID `com.supercell.brawlstarx` and requests INTERNET permission. It currently exits during startup and is not playable. Install all five splits together; the official Supercell game remains a separate package.

The APKs are versioned release assets. The local debug signing key is not published, so a rebuild signed with a different key requires reinstalling the client copy.

[Client development notes](APK32/DEVELOPMENT.md) record completed work and remaining issues. Generated files, logs, reference APKs from other apps and signing keys are excluded from Git. The included patch scripts are experimental and do not yet form a complete portable build system.
