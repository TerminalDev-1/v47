#ifndef PRIVATE_SERVER_REDIRECT_ADDRESS_H
#define PRIVATE_SERVER_REDIRECT_ADDRESS_H

/* Android ARM is little-endian. Return the sockaddr size, or zero if unchanged. */
static unsigned int redirect_address(unsigned char out[28], const unsigned char *in, unsigned int length) {
    if (!in || length < 8 || in[1] != 0 || in[2] != 0x24 || in[3] != 0x7b) return 0;
    for (unsigned int i = 0; i < 28; ++i) ((volatile unsigned char *)out)[i] = 0;
    if (in[0] == 2 && length >= 16) {
        out[0] = 2; out[2] = 0x24; out[3] = 0x7b;
        out[4] = 127; out[7] = 1;
        return 16;
    }
    if (in[0] == 10 && length >= 28) {
        out[0] = 10; out[2] = 0x24; out[3] = 0x7b;
        out[23] = 1; /* ::1 */
        return 28;
    }
    return 0;
}
#endif
