# Observed 47.227 protocol

The physical tablet client reaches the local service through ADB reverse on port 19347. Its captured exchange is:

1. ClientHello 10100: 72 bytes, message version 0.
2. ServerHello 20100: a big-endian length of 24 followed by a random 24-byte session token.
3. Login 10101: 302 bytes, message version 10; encrypted.

ClientHello fields observed: protocol 2, key version 35, client major 47, minor 0, build 227, a 40-character resource fingerprint, device/app-store integers 2 and 2.

`server/crypto.py` implements the authenticated login envelope and subsequent symmetric transport. Its client-simulation tests pass, including token validation, tamper rejection, nonce advancement and bidirectional messages. This is not yet proof of interoperability with the tablet: the client must use the matching server public key before login can be decrypted.

`server/accounts.py` persists account IDs and random tokens in SQLite. Account data and protocol captures are ignored by Git.

The next acceptance test is actual tablet Login decryption, followed by LoginOk (20104) and a client-validated OwnHomeData (24101). No home-screen success has been claimed.
