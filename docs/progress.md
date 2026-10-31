# Current integration status

Target: 47.227, ARM64. Physical tablet: f298358c. Separate package: com.supercell.brawlstarq.

## Verified

The automatic embedded startup script removes the diagnostic wait and resolves the signature-related crash in the cloned client. Three cold starts succeeded without a tracing controller. The original official game remains untouched.

Server framing tests pass. The physical tablet USB tunnel returns ServerHello to a synthetic ClientHello. The server supports 10100/20100 and 10108/20108. It is not yet a complete game service.

## Current work

Persistently redirect the cloned client's game connection to localhost:19347 through ADB reverse, capture the actual ClientHello and Login, then implement login crypto, LoginOk (20104), and OwnHomeData (24101). Reach the actual home screen on the physical tablet before marking this objective complete.

A public source advertised as v47 contains v44 version checks and must not be treated as a verified matching schema.

## Home-data service implementation

The physical client sent 10100 and encrypted 10101 to the service through USB. The service now has a full connection state machine, authenticated login, persistent account IDs/tokens, LoginOk (20104), OwnHomeData (24101), and encrypted keepalive. The v47.227 serializers are adapted from itswester/Brawl-Stars-v47 commit 09acf78802b7faf60bc6850ed976e682741652e9 under Apache-2.0; attribution and license are in server/schemas.

Thirteen tests pass, including client-simulated authenticated login, decrypted home response, and encrypted heartbeat. The tablet has not yet accepted LoginOk or reached the home screen: matching client/server key configuration remains unresolved. The heavy tracing build was removed after audio disruption, and the user confirmed normal audio on the restored build. Do not reintroduce continuous memory-copy tracing.
