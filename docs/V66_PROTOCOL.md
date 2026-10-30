# V66 protocol notes

These are observations from the [KSBS-V66 reference implementation](https://github.com/KasyaGamer/KSBS-V66), whose README targets **66.293**. They are starting points for the Python server; none has been verified with our 66.300 client.

- Its network code reads a seven-byte header: a two-byte message ID, a three-byte payload length, and a two-byte message version, all big-endian.
- Its message factory identifies ClientHello as `10100` and replies with ServerHello `20100`, version `0`. The example does not decode the ClientHello payload.
- Its ServerHello writes a big-endian integer `24` followed by 24 bytes of value `1`. This is the example's behavior; it does not establish the right challenge or encryption for an unmodified 66.300 client.
- Its Login message is `10101` and its decoder reads two 32-bit account fields, a string, and three variable-length integers. Compatibility and encryption behavior for our client remain unverified.

The repository describes itself as a test project with missing features and provides a separate client. We should not assume an unmodified APK will speak the same wire format or that the reference provides a complete protocol specification.
