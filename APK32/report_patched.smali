.class public Lelsm/o;
.super Ljava/lang/Object;
.source "SourceFile"


# static fields
.field private static final a:Ljava/lang/String; = "Report"

.field private static b:I = -0x1


# direct methods
.method static constructor <clinit>()V
    .locals 0

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static a(Ljava/lang/String;)Lelsm/az;
    .locals 3

    const-string v0, "!"

    if-nez p0, :cond_0

    new-instance p0, Lelsm/G;

    invoke-direct {p0, v0}, Lelsm/G;-><init>(Ljava/lang/String;)V

    return-object p0

    :cond_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v1

    const/4 v2, 0x2

    if-ge v1, v2, :cond_1

    new-instance v1, Lelsm/G;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    invoke-direct {v1, p0}, Lelsm/G;-><init>(Ljava/lang/String;)V

    return-object v1

    :cond_1
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v0

    if-eqz v0, :cond_2

    new-instance v0, Lelsm/G;

    invoke-direct {v0, p0}, Lelsm/G;-><init>(Ljava/lang/String;)V

    return-object v0

    :cond_2
    const/4 v0, 0x0

    invoke-virtual {p0, v0, v2}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v0

    const/16 v1, 0x10

    invoke-static {v0, v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result v0

    packed-switch v0, :pswitch_data_0

    :pswitch_0
    new-instance v0, Lelsm/G;

    invoke-direct {v0, p0}, Lelsm/G;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_1
    new-instance v0, Lelsm/ax;

    invoke-direct {v0, p0}, Lelsm/ax;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_2
    new-instance v0, Lelsm/ag;

    invoke-direct {v0, p0}, Lelsm/ag;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_3
    new-instance v0, Lelsm/T;

    invoke-direct {v0, p0}, Lelsm/T;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_4
    new-instance v0, Lelsm/aB;

    invoke-direct {v0, p0}, Lelsm/aB;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_5
    new-instance v0, Lelsm/c;

    invoke-direct {v0, p0}, Lelsm/c;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_6
    new-instance v0, Lelsm/aC;

    invoke-direct {v0, p0}, Lelsm/aC;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_7
    new-instance v0, Lelsm/U;

    invoke-direct {v0, p0}, Lelsm/U;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_8
    new-instance v0, Lelsm/an;

    invoke-direct {v0, p0}, Lelsm/an;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_9
    new-instance v0, Lelsm/B;

    invoke-direct {v0, p0}, Lelsm/B;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_a
    new-instance v0, Lelsm/Q;

    invoke-direct {v0, p0}, Lelsm/Q;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_b
    new-instance v0, Lelsm/s;

    invoke-direct {v0, p0}, Lelsm/s;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_c
    new-instance v0, Lelsm/aD;

    invoke-direct {v0, p0}, Lelsm/aD;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_d
    new-instance v0, Lelsm/R;

    invoke-direct {v0, p0}, Lelsm/R;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_e
    new-instance v0, Lelsm/u;

    invoke-direct {v0, p0}, Lelsm/u;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_f
    new-instance v0, Lelsm/C;

    invoke-direct {v0, p0}, Lelsm/C;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_10
    new-instance v0, Lelsm/r;

    invoke-direct {v0, p0}, Lelsm/r;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_11
    new-instance v0, Lelsm/aj;

    invoke-direct {v0, p0}, Lelsm/aj;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_12
    new-instance v0, Lelsm/av;

    invoke-direct {v0, p0}, Lelsm/av;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_13
    new-instance v0, Lelsm/P;

    invoke-direct {v0, p0}, Lelsm/P;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_14
    new-instance v0, Lelsm/w;

    invoke-direct {v0, p0}, Lelsm/w;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_15
    new-instance v0, Lelsm/g;

    invoke-direct {v0, p0}, Lelsm/g;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_16
    new-instance v0, Lelsm/af;

    invoke-direct {v0, p0}, Lelsm/af;-><init>(Ljava/lang/String;)V

    return-object v0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_16
        :pswitch_15
        :pswitch_14
        :pswitch_13
        :pswitch_12
        :pswitch_11
        :pswitch_10
        :pswitch_f
        :pswitch_e
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_d
        :pswitch_0
        :pswitch_c
        :pswitch_b
        :pswitch_a
        :pswitch_9
        :pswitch_d
        :pswitch_0
        :pswitch_d
        :pswitch_8
        :pswitch_7
        :pswitch_6
        :pswitch_5
        :pswitch_0
        :pswitch_4
        :pswitch_3
        :pswitch_2
        :pswitch_1
    .end packed-switch
.end method

.method private static a()Ljava/lang/String;
    .locals 7

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const/4 v1, 0x0

    :try_start_0
    sget v2, Lelsm/o;->b:I

    invoke-static {v2}, Landroid/os/ParcelFileDescriptor;->adoptFd(I)Landroid/os/ParcelFileDescriptor;

    move-result-object v2

    new-instance v3, Landroid/os/ParcelFileDescriptor$AutoCloseInputStream;

    invoke-direct {v3, v2}, Landroid/os/ParcelFileDescriptor$AutoCloseInputStream;-><init>(Landroid/os/ParcelFileDescriptor;)V

    new-instance v2, Ljava/io/BufferedReader;

    new-instance v4, Ljava/io/InputStreamReader;

    invoke-direct {v4, v3}, Ljava/io/InputStreamReader;-><init>(Ljava/io/InputStream;)V

    invoke-direct {v2, v4}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_2
    .catchall {:try_start_0 .. :try_end_0} :catchall_1

    const/16 v3, 0x400

    :try_start_1
    new-array v4, v3, [C

    :cond_0
    const/4 v5, 0x0

    invoke-virtual {v2, v4, v5, v3}, Ljava/io/BufferedReader;->read([CII)I

    move-result v6

    if-lez v6, :cond_1

    invoke-virtual {v0, v4, v5, v6}, Ljava/lang/StringBuilder;->append([CII)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    const-string v6, "?"

    invoke-virtual {v5, v6}, Ljava/lang/String;->endsWith(Ljava/lang/String;)Z

    move-result v5

    if-eqz v5, :cond_0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->length()I

    move-result v3

    add-int/lit8 v3, v3, -0x1

    invoke-virtual {v0, v3}, Ljava/lang/StringBuilder;->setLength(I)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    goto :goto_0

    :catchall_0
    move-exception v0

    move-object v1, v2

    goto :goto_2

    :catch_0
    nop

    goto :goto_3

    :cond_1
    :goto_0
    :try_start_2
    invoke-virtual {v2}, Ljava/io/BufferedReader;->close()V
    :try_end_2
    .catch Ljava/lang/Exception; {:try_start_2 .. :try_end_2} :catch_1

    goto :goto_1

    :catch_1
    nop

    :goto_1
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->length()I

    move-result v2

    if-gtz v2, :cond_2

    return-object v1

    :cond_2
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :catchall_1
    move-exception v0

    goto :goto_2

    :catch_2
    nop

    move-object v2, v1

    goto :goto_3

    :goto_2
    if-eqz v1, :cond_3

    :try_start_3
    invoke-virtual {v1}, Ljava/io/BufferedReader;->close()V
    :try_end_3
    .catch Ljava/lang/Exception; {:try_start_3 .. :try_end_3} :catch_3

    :catch_3
    :cond_3
    throw v0

    :goto_3
    if-eqz v2, :cond_4

    :try_start_4
    invoke-virtual {v2}, Ljava/io/BufferedReader;->close()V
    :try_end_4
    .catch Ljava/lang/Exception; {:try_start_4 .. :try_end_4} :catch_4

    :catch_4
    :cond_4
    return-object v1
.end method

.method static synthetic b()I
    .locals 1

    sget v0, Lelsm/o;->b:I

    return v0
.end method

.method public static b(Ljava/lang/String;)V
    .locals 0
    return-void
.end method

.method static synthetic c()Ljava/lang/String;
    .locals 1

    invoke-static {}, Lelsm/o;->a()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public static d()V
    .locals 1

    new-instance v0, Lelsm/O;

    invoke-direct {v0}, Lelsm/O;-><init>()V

    invoke-virtual {v0}, Ljava/lang/Thread;->start()V

    return-void
.end method
