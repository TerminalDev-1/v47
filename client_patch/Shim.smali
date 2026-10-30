.class public Lcom/privateserver/Shim;
.super Ljava/lang/Object;

.method public static load()V
    .locals 1
    const-string v0, "pshook"
    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V
    return-void
.end method

.method public static native preloadShield()V
.end method

.method public static native patchShield()V
.end method

.method public static native patchGame()V
.end method
