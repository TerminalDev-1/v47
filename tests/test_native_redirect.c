#include <assert.h>
#include "../client_patch/redirect_address.h"
int main(void) {
    unsigned char out[28], v4[16] = {2,0,0x24,0x7b,8,8,8,8};
    unsigned char v6[28] = {10,0,0x24,0x7b,0,0,0,0,0x20,1};
    assert(redirect_address(out,v4,16)==16 && out[0]==2 && out[4]==127 && out[7]==1);
    assert(redirect_address(out,v6,28)==28 && out[0]==10 && out[8]==0 && out[23]==1);
    assert(redirect_address(out,v6,16)==0);
    v4[3]=0x7c; assert(redirect_address(out,v4,16)==0);
    assert(redirect_address(out,0,0)==0);
    return 0;
}
