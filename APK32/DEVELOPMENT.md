# Client development — 69.414

The official tablet installation remains `com.supercell.brawlstars` (ARM64). The separate test clone is `com.supercell.brawlstarx` (ARM32). The currently installed test clone has INTERNET permission restored and is stopped. Do not treat it as a working client.

## Reproduced findings

- The original package rename changed a package-visibility query as well as the manifest package. The protection then called `PackageManager.getApplicationInfo("com.supercell.brawlstars", ...)`, which threw because the original package was not visible. Its native initializer returned JNI_ERR. `fix_query.py` restores that query with a distinct binary XML string while retaining the clone ID; this got past that original error.
- With original visibility restored and unmodified native code, protection reported `elsm.g: 01`. With injected Frida and the same query, it reported `elsm.B: 16`. The precise meaning of either code is unconfirmed. Frida changes the behavior, so conclusions drawn from it must be confirmed without instrumentation.
- In a deliberately offline test, changing `elsm/o.b(String)` to return without invoking the default uncaught-exception handler, together with the query fix, let the process load `libg.so`, initialize audio and load Flutter/SCID components. It then died from SIGKILL within a few seconds. No playable screen or connection to the server was verified.
- In one instrumented offline test, native code called `tgkill` repeatedly to send SIGKILL to threads in its own process. Suppressing those calls was insufficient: the process exited cleanly with status 1. Patching an exit wrapper earlier caused a native crash. Avoid assuming there is only one shutdown mechanism.
- The native bootstrap is unpacked in memory. Post-unpack ARM32 snapshots are `bootstrap_runtime_text.bin` (base-relative 0x440000) and `bootstrap_400000.bin` (base-relative 0x400000). They are diagnostic snapshots, not replacement libraries.
- The tablet also has Null's 69.252 and BSD 69.230, pulled under `reference/` for comparison. The Null's ARM32 `GameApp` native method declarations match 69.414's declarations, but this does not establish binary compatibility; no reference library has been substituted into the stock client.

## Artifacts

- `query_fixed_signed/`: signed base with fixed package visibility; original ARM32 split and asset/language/density splits are under `signed/`.
- `offline_test_signed/`: signed base with package visibility fix, reporting-method experiment, and INTERNET permission removed. This was used for the offline isolation test. Its source procedure is in `build_offline_test.py`, with decoded sources under `smali/`.
- `instrumented_signed/` and `gadget_probe.js`: temporary debugging builds. They are unstable and must not be treated as release builds. Frida can provoke additional checks; the test clone must stay offline while destinations are not verified.
- `Private Server/server.py`: loopback-only hello listener. An independent v69-format reference client completed ClientHello and ServerHello; the real Android client has not yet done so. USB forwarding is `adb -d reverse tcp:9339 tcp:9339`.

Next: identify and neutralize the remaining protection shutdown without losing the registered native methods, then verify a client endpoint redirect and observe real v69 handshake frames. Keep originals and the official installed game intact.

- After the user requested it, INTERNET was restored in `online_test_signed/` and confirmed granted by Android. A launch still ended in SIGKILL; the server received no game connection. The client's destination has not yet been redirected to localhost.

## USB redirect

An experimental connect hook for port 9339 is in `client_patch/redirect.js`. A controlled socket aimed at a test address was redirected to 127.0.0.1:9339, forwarded by USB ADB, and delivered a synthetic frame to the Python listener. The actual game has not yet connected: it exits during protection startup, and its v69 server port and protocol remain unverified. INTERNET remains granted.

The newer native bootstrap in `client_patch/native_redirect.c` avoids Frida and patches version-specific imports. It still reports protection code `01` and exits; spoofing the original signed base path did not resolve that. The code originates through a shared JNI string wrapper, which does not identify the underlying failing check. The currently installed test clone uses this experimental native bootstrap and is stopped. No real Android ClientHello has been observed.

On a later USB test, stack candidates and a runtime code snapshot placed the first `01` report on a call path through native offsets `0x191208`, `0x191018`, `0x1913ac`, and `0x19164e`. These are observations in the unpacked ARM32 protection library, not the location of the underlying failed check. Temporarily skipping a later report branch at `0x1913ee` suppressed a repeat report but did not prevent the first shutdown attempt or a subsequent clean exit with status 1. The branch experiment was removed, and the baseline experimental clone was reinstalled and stopped. Further work must address the initiating check or the separate exit path, not simply suppress repeated reports.

Additional USB tests found that returning the original package name to the protection library and holding its signal-sending thread both failed to prevent startup exit. The protection library's imported `exit` function was not called in the observed run, so the separate exit path is still unidentified. An attempted process-wide libc exit hook caused a native crash and was removed. Before the first report, protection reads the application package, source, data and native-library paths and looks up package information; none alone establishes the cause of `01`.

Further startup experiments skipped selected protected class registrations. That got past some Android initializers but broke protected configuration values, first causing a null connectivity manager and later a consent SDK initialization error; these bypasses were reverted. Hiding the injected shim from the native library directory listing did not clear code `01`. Loading the shim from external storage failed Android's native-library namespace check, so that experiment was reverted as well. The normal experimental clone was reinstalled and stopped after testing.

Another temporary clone build enabled Android's debuggable flag, but `strace` could not attach even as the app UID (`PTRACE_SEIZE: Operation not permitted`); `debuggerd` also required root on this tablet. Spoofing both the original package name and its data-directory path did not clear `01`. The signed original base copied to the clone's external files directory was verified byte-for-byte by SHA-256. These tests did not modify the official app or tablet-wide debugging settings, and the non-debuggable experimental clone was restored afterward.

A deeper stack scan identified a call at runtime offset `0x137ba4` that passes error code 1 to the reporting path. Skipping that call, or replacing its containing function's return value shortly after unpacking, caused rapid signal-9 termination rather than a working startup. Neither patch was retained. The native build installer now checks the expected original base APK hash and copies it to the clone's files directory over USB, so a fresh install does not depend on a previous manual transfer.

An unpacked runtime snapshot also contains ARM syscall wrappers for `exit_group` at `0x456650` and `kill` at `0x465c50`. Attempts to trace those by changing their instructions either crashed during unpacking or caused rapid signal-9 termination before a trace was captured. Those hooks were removed; the presence of the wrappers does not prove which one caused the observed exit. A less intrusive way to trace that path is still needed.

The native port-9339 redirect now preserves the socket family: IPv4 is redirected to `127.0.0.1`, and IPv6 to `::1`. The USB reverse forwarding accepted a direct IPv6 loopback connection in a separate test. This does not establish which address family or port the actual game uses.

`tests/android_native_probe.c` is a standalone synthetic ARM32 test, not the game client. On the tablet it used the same native address-rewrite helper and completed ClientHello/ServerHello over USB with both IPv4 and IPv6. To repeat with the local Zig toolchain and a running server: `tools/ziglang/ziglang/zig.exe cc -target arm-linux-android -mcpu=cortex_a7 -marm -O0 -fno-stack-protector -static -nostdlib -Wl,-e,_start -o build/android_native_probe tests/android_native_probe.c`, then push it to `/data/local/tmp`, mark it executable, and run it using `adb -d`.
