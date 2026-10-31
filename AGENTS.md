# v47 development instructions

This repository targets Brawl Stars 47.227. The main goal is a working private server that reaches OwnHomeData (24101) on the USB-connected physical tablet.

Use explicit ADB device serial f298358c. Do not use an emulator. Preserve the original APK and official installed game and its data; use com.supercell.brawlstarq for the private client. Keep the automatic startup fix working across cold starts. Do not restore a diagnostic build that waits for a debugger.

Implement and verify the actual client/server handshake and login before claiming home-screen support. Keep protocol captures and generated APKs out of Git. A packet emitted by a synthetic test is not evidence that the game client connected. Version-labelled reference servers must be checked against their source and the actual client before adoption.

Commit and push meaningful verified source progress during development, and continue working after checkpoints. Do not publish secrets, original APKs, generated client artifacts or session captures.
