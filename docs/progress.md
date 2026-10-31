# Current integration status

Target: 47.227, ARM64. Physical tablet: f298358c. Separate package: com.supercell.brawlstarq.

## Verified

The automatic embedded startup script removes the diagnostic wait and resolves the signature-related crash in the cloned client. Three cold starts succeeded without a tracing controller. The original official game remains untouched.

Server framing tests pass. The physical tablet USB tunnel returns ServerHello to a synthetic ClientHello. The server supports 10100/20100 and 10108/20108. It is not yet a complete game service.

## Current work

Persistently redirect the cloned client's game connection to localhost:19347 through ADB reverse, capture the actual ClientHello and Login, then implement login crypto, LoginOk (20104), and OwnHomeData (24101). Reach the actual home screen on the physical tablet before marking this objective complete.

A public source advertised as v47 contains v44 version checks and must not be treated as a verified matching schema.
