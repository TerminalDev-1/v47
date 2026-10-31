# Brawl Stars v47 private server

Target client: **47.227**. The current objective is to reach the home screen through a locally hosted server and `OwnHomeData` (24101).

The separately installed tablet client is `com.supercell.brawlstarq`. Its automatic startup patch preserves the original game library and bytecode, and supplies the original certificate to the cloned app's startup checks. Test only on the USB-connected physical tablet; preserve the official installed game and its data.

## Run

```powershell
python -m unittest discover -s server -p test_protocol.py -v
python -u server/main.py
adb -s f298358c reverse tcp:19347 tcp:19347
```

The service implements framing, ClientHello/ServerHello, authenticated login, persistent accounts, LoginOk (20104), OwnHomeData (24101), and encrypted keepalive. Thirteen tests pass, including the complete encrypted login-to-home response sequence. The physical game client has sent encrypted Login to this service; its matching server-key configuration and actual home-screen decoding are still being verified.

## Client

- `tools/startup.js`: automatic startup checks and backend routing.
- `tools/build_autostart.py`: packages the embedded script into the diagnostic base.
- Signed APKs, original client assets, captures and local build tools stay outside Git.

The original 47.227 APK remains unmodified in the project folder. Startup was verified across three cold starts without a debugger attached. The routed client now sends real ClientHello and Login messages to the local service. Login authentication with the service key is the current integration blocker.

The server foundations now include authenticated transport (`server/crypto.py`), bounded binary streams (`server/stream.py`) and persistent accounts (`server/accounts.py`). Run all checks with `python -m unittest discover -s server -p "test_*.py" -v`. Install dependencies with `python -m pip install -r requirements.txt`.

The real tablet handshake has been captured through encrypted Login; details and the remaining key-configuration step are in `docs/protocol.md`.
