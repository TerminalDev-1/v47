/* 69.414 ARM32 private-server bootstrap. Experimental, exact build only. */
#include "redirect_address.h"
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned long uptr;
typedef unsigned int usize;
typedef unsigned int pthread_t;
struct phdrinfo { uptr addr; const char *name; const void *phdr; u16 phnum; };
struct sockaddr { u16 family; unsigned char data[14]; };
extern int dl_iterate_phdr(int (*callback)(struct phdrinfo *, usize, void *), void *);
extern void *dlopen(const char *, int);
extern const char *dlerror(void);
extern int mprotect(void *, usize, int);
extern int pthread_create(pthread_t *, const void *, void *(*)(void *), void *);
extern int __android_log_write(int, const char *, const char *);
extern int strcmp(const char *, const char *);
extern int getpid(void);
extern int snprintf(char *, usize, const char *, ...);
extern void pthread_exit(void *);
extern int usleep(unsigned int);
#define LOG(s) __android_log_write(4, "PrivateServerNative", s)
#define READ 1
#define WRITE 2
static uptr shield_base, game_base;
static int (*original_create)(pthread_t *, const void *, void *(*)(void *), void *);
static int (*original_tgkill)(int, int, int);
static int (*original_connect)(int, const struct sockaddr *, u32);
static int patched_shield, patched_game;
static volatile int game_lock;
static volatile int app_info_spoofed;
static void *(*original_new_string)(void *, const char *);
static void *(*original_get_field_id)(void *, void *, const char *, const char *);
static void *(*original_get_object_field)(void *, void *, void *);
static void *source_field, *public_source_field;
static int from_shield(uptr caller) {
 return shield_base && caller>=shield_base && caller<shield_base+0x4d0000;
}
static void *get_field_id_guard(void *env, void *cls, const char *name, const char *sig) {
 void *id=original_get_field_id(env,cls,name,sig);
 if(from_shield((uptr)__builtin_return_address(0)) && name && sig && !strcmp(sig,"Ljava/lang/String;")) {
  if(!strcmp(name,"sourceDir")){source_field=id;LOG("observed application sourceDir field");}
  if(!strcmp(name,"publicSourceDir")){public_source_field=id;LOG("observed application publicSourceDir field");}
 }
 return id;
}
static void *get_object_field_guard(void *env, void *object, void *field) {
 if(from_shield((uptr)__builtin_return_address(0)) && field &&
    (field==source_field || field==public_source_field)) {
  LOG("providing original signed base for protection verification");
  return original_new_string(env,"/sdcard/Android/data/com.supercell.brawlstarx/files/original_base.apk");
 }
 return original_get_object_field(env,object,field);
}
static void *new_string_guard(void *env, const char *value) {
 uptr caller=(uptr)__builtin_return_address(0);
 if(from_shield(caller) && value && !strcmp(value,"01")) {
  char b[96];snprintf(b,sizeof(b),"protection code 01 created at offset 0x%lx",caller-shield_base);LOG(b);
 }
 if(shield_base && caller>=shield_base && caller<shield_base+0x4d0000 && value &&
    !strcmp(value,"com.supercell.brawlstars") &&
    __sync_bool_compare_and_swap(&app_info_spoofed,0,1)) {
  LOG("using clone application info for ARM32 startup");
  return original_new_string(env,"com.supercell.brawlstarx");
 }
 return original_new_string(env,value);
}
__attribute__((visibility("default"))) void Java_com_privateserver_Shim_patchGame(void *,void *);
static void *watch_game(void *unused) {
 (void)unused;
 for (int i=0;i<30000 && !patched_game;i++) {
  Java_com_privateserver_Shim_patchGame((void *)0,(void *)0);
  if(!patched_game)usleep(1000);
 }
 return (void *)0;
}
static const char *lastpart(const char *s) { const char *last=s; if(!s)return ""; while(*s){if(*s=='/')last=s+1;s++;}return last; }
static int find_module(struct phdrinfo *i, usize size, void *unused) {
 (void)size; (void)unused; const char *n=lastpart(i->name);
 if(!strcmp(n,"libsupercell_brawlstars.so"))shield_base=i->addr;
 if(!strcmp(n,"libg.so"))game_base=i->addr;
 return 0;
}
static int replace_slot(uptr addr, void *replacement, void **old) {
 uptr page=addr & ~(uptr)4095; void **slot=(void **)addr;
 if(*slot==replacement)return 1;
 if(mprotect((void *)page,4096,READ|WRITE)!=0){LOG("unable to modify import slot");return 0;}
 *old=*slot; *slot=replacement;
 if(mprotect((void *)page,4096,READ)!=0)LOG("could not restore import protection");
 return 1;
}
static void *harmless(void *arg){(void)arg;return (void *)0;}
static int create_guard(pthread_t *t,const void *attr,void *(*start)(void *),void *arg) {
 uptr offset=((uptr)start & ~(uptr)1)-shield_base;
 if(offset<0x4d0000){char b[96];snprintf(b,sizeof(b),"protection thread start offset 0x%lx",offset);LOG(b);}
 if(offset==0x34bb34){LOG("suppressed protection shutdown worker");return original_create(t,attr,harmless,arg);}
 return original_create(t,attr,start,arg);
}
static int tgkill_guard(int process,int thread,int sig) {
 if(process==getpid()&&sig==9){char b[128];uptr caller=(uptr)__builtin_return_address(0);snprintf(b,sizeof(b),"stopping protection termination thread: caller 0x%lx",caller-shield_base);LOG(b);pthread_exit((void *)0);return 0;}
 return original_tgkill(process,thread,sig);
}
static int connect_local(int fd,const struct sockaddr *address,u32 len) {
 unsigned char local[28];
 u32 local_len=redirect_address(local,(const unsigned char *)address,len);
 if(local_len){LOG("redirecting game port to USB listener");return original_connect(fd,(const struct sockaddr *)local,local_len);}
 return original_connect(fd,address,len);
}
__attribute__((visibility("default"))) void Java_com_privateserver_Shim_patchShield(void *env,void *cls) {
 (void)env;(void)cls;dl_iterate_phdr(find_module,(void *)0);
 if(!shield_base){LOG("shield module not yet loaded");return;}
 if(!patched_shield){int a=replace_slot(shield_base+0x4b63a8,(void *)create_guard,(void **)&original_create);int b=replace_slot(shield_base+0x4b65e0,(void *)tgkill_guard,(void **)&original_tgkill);patched_shield=a&&b;if(patched_shield){pthread_t t;LOG("protection imports patched");pthread_create(&t,(void *)0,watch_game,(void *)0);}}
}
__attribute__((visibility("default"))) void Java_com_privateserver_Shim_preloadShield(void *env,void *cls) {
 (void)cls;
 void *handle=dlopen("libsupercell_brawlstars.so",2);
 if(!handle){const char *error=dlerror();if(error)__android_log_write(6,"PrivateServerNative",error);return;}
 LOG("protection library preloaded");
 Java_com_privateserver_Shim_patchShield((void *)0,(void *)0);
 if(env){uptr table=*(uptr *)env;
  if(replace_slot(table+167*4,(void *)new_string_guard,(void **)&original_new_string))LOG("package lookup hook installed");
  if(replace_slot(table+94*4,(void *)get_field_id_guard,(void **)&original_get_field_id) &&
     replace_slot(table+95*4,(void *)get_object_field_guard,(void **)&original_get_object_field))LOG("application-info field hooks installed");
 }
}
__attribute__((visibility("default"))) void Java_com_privateserver_Shim_patchGame(void *env,void *cls) {
 (void)env;(void)cls;dl_iterate_phdr(find_module,(void *)0);
 if(!game_base||patched_game)return;
 if(__sync_lock_test_and_set(&game_lock,1))return;
 if(patched_game){__sync_lock_release(&game_lock);return;}
 patched_game=replace_slot(game_base+0x1022af4,(void *)connect_local,(void **)&original_connect);
 __sync_lock_release(&game_lock);
 if(patched_game)LOG("game connect import patched");
}
