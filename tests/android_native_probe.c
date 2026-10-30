#include "../client_patch/redirect_address.h"
static int sc3(int nr,int a,int b,int c){register int r0 __asm__("r0")=a,r1 __asm__("r1")=b,r2 __asm__("r2")=c,r7 __asm__("r7")=nr;__asm__ volatile("svc 0":"+r"(r0):"r"(r1),"r"(r2),"r"(r7):"memory");return r0;}
static int run(int family) {
 unsigned char dest[28]={0},out[28],reply[35],frame[39]={0};
 dest[0]=family;dest[2]=0x24;dest[3]=0x7b;dest[4]=203;dest[6]=113;dest[7]=1;
 int n=redirect_address(out,dest,family==2?16:28);
 int fd=sc3(281,family,1,0);if(fd<0 || !n)return 1;
 if(sc3(283,fd,(int)out,n)!=0)return 2;
 frame[0]=0x27;frame[1]=0x74;frame[4]=32;
 frame[10]=2;frame[14]=59;frame[18]=69;frame[22]=1;frame[25]=1;frame[26]=0x9e;
 frame[34]=2;frame[38]=2;
 if(sc3(4,fd,(int)frame,sizeof(frame))!=sizeof(frame))return 3;
 int got=0;while(got<35){int r=sc3(3,fd,(int)(reply+got),35-got);if(r<=0)return 4;got+=r;}
 if(reply[0]!=0x4e||reply[1]!=0x84||reply[4]!=28||reply[7]!=0||reply[8]!=0||reply[9]!=0||reply[10]!=24)return 5;
 sc3(6,fd,0,0);return 0;
}
void _start(void){int a=run(2),b=run(10);if(a||b){char msg[]="Synthetic ARM32 hello failed\n";sc3(4,1,(int)msg,sizeof(msg)-1);sc3(248,10*a+b,0,0);}else{char msg[]="Synthetic ARM32 IPv4 and IPv6 hello passed\n";sc3(4,1,(int)msg,sizeof(msg)-1);sc3(248,0,0,0);}for(;;){}}
