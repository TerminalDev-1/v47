# Brawl Stars V66 Private Server Implementation

Private Server is an early-stage Python private-server project for Brawl Stars V66, the Prestige update. The V66 client and server are not working together yet. There is no server implementation in this workspace; development starts from the APK and protocol references below.

## Client

The provided APKPure bundle identifies itself as Brawl Stars **66.300** (`com.supercell.brawlstars`, version code `66300`). It contains a single ARM64 split, `config.arm64_v8a.apk`, and no ARM32 split. The game library (`libg.so`) and the protection library (`libsupercell_brawlstars.so`) are both 64-bit ARM. The original XAPK and extracted splits are in `APK/` and are excluded from Git. USB debugging (`adb -d`) is the preferred way to test on the tablet; preserve the official installation and use a separately identified test copy.

## Protocol reference

[KSBS-V66](https://github.com/KasyaGamer/KSBS-V66) is a public Node.js server example for **66.293**. Its source archive contains packet implementations including ClientHello (10100), ServerHello (20100), login, and home messages. Its README describes it as a testing project with incomplete functionality. It is a useful reference, but compatibility with **66.300** and the provided APK has not been established. Our server is intended to be written in Python.

## Why we switched from V69

The V69 client did not reach its connecting screen: the separately packaged ARM32 clone stopped during protected startup before sending a real ClientHello. Several approaches failed to make it usable, and further work would require disproportionate time and compute for the current goal. V69 is paused for possible future work in the separate [V69 research repository](https://github.com/TerminalDev-1/brawl-stars-v69-research).

This repository was renamed from the V69 project, so its Git history and [legacy V69 release](https://github.com/TerminalDev-1/brawl-stars-v66-private-server/releases/tag/v0.1.0-investigation) still contain the earlier work. Those release files are not V66 clients.
