from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
base = root / 'APK32' / 'smali'

def replace_method(path, signature, replacement):
    text = path.read_text(encoding='utf-8')
    pattern = r'(?ms)^\.method ' + re.escape(signature) + r'\s*\n.*?^\.end method'
    text, count = re.subn(pattern, lambda _: replacement, text)
    if count != 1:
        raise SystemExit(f'Expected one {signature} in {path}, found {count}')
    path.write_text(text, encoding='utf-8')

shim = base / 'smali_classes2/com/privateserver/Shim.smali'
shim.parent.mkdir(parents=True, exist_ok=True)
shim.write_text((root / 'client_patch/Shim.smali').read_text(encoding='utf-8'), encoding='utf-8')
replace_method(base / 'smali_classes2/elsm/M.smali', 'private static d()V', '''.method private static d()V
    .locals 1
    invoke-static {}, Lcom/privateserver/Shim;->load()V
    invoke-static {}, Lcom/privateserver/Shim;->preloadShield()V
    const-string v0, "supercell_brawlstars"
    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V
    invoke-static {}, Lcom/privateserver/Shim;->patchShield()V
    return-void
.end method''')
path = base / 'smali_classes2/elsm/K.smali'
text = path.read_text(encoding='utf-8')
call = '    invoke-static {}, Lcom/privateserver/Shim;->patchGame()V'
if call not in text:
    pattern = r'(\.method public static a\(I\)Ljava/lang/String;\s+\.locals 1)'
    text, count = re.subn(pattern, lambda m: m.group(1) + '\n\n' + call, text)
    if count != 1:
        raise SystemExit('Could not locate game hook insertion point')
    path.write_text(text, encoding='utf-8')
replace_method(base / 'smali_classes2/elsm/o.1.smali', 'public static b(Ljava/lang/String;)V', '''.method public static b(Ljava/lang/String;)V
    .locals 0
    return-void
.end method''')
print('Prepared experimental native bootstrap in secondary dex')
