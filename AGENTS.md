# Private Server

This is an early-stage Python private-server project targeting Brawl Stars V66, the Prestige update. Inspect the workspace and APK before assuming server code exists. The retained client is version 66.300 ARM32, in `APK/BrawlStars_66.300_armeabi-v7a.xapk`, with extracted splits in `APK/v66.300-arm32/`. Do not assume reference implementations for 66.293 are compatible. Build the client and server components needed for the project. Preserve original APKs and the official installed game, and use a separately identified test copy. Prefer USB debugging (`adb -d`) for tablet work. Verify actual client and protocol behavior.

## Next work

The V66 client has not yet been patched, installed as a separate clone, connected to a private server, or tested on the tablet. No V66 server implementation exists in this workspace. Start by patching the ARM32 client: preserve INTERNET permission, create a distinct package ID so it can coexist with the official game, redirect the game connection to a local test server, and use USB debugging to test it. The immediate goal is to reach the connecting screen and observe a real ClientHello; then implement and verify the Python server's ServerHello and remaining protocol. Do not connect the test client to official game servers. The protection library is present, and no claim has been established that V66 is easier to patch.

The V66 protocol notes in `docs/V66_PROTOCOL.md` describe a 66.293 reference implementation. They are starting points, not proof of compatibility with 66.300. The old V69 test clone was removed from the tablet; the official game remains installed. The user removed the V66 ARM64 bundle and splits, so keep the remaining ARM32 originals intact.

The V69 project is paused at https://github.com/TerminalDev-1/brawl-stars-v69-research; do not treat it as the V66 implementation. Commit and push meaningful, verified progress during development and continue working in the same turn. Preserve unrelated changes and avoid publishing secrets or generated artifacts.
