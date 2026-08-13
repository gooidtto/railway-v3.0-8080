#!/usr/bin/env python3
import hashlib,json,os,sys,tarfile,time
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit("usage: backup_state.py DATA_DIR CONFIG")
root=Path(sys.argv[1]).resolve(); config=Path(sys.argv[2]).resolve(); backup_root=root/"backups"; backup_root.mkdir(mode=0o700,parents=True,exist_ok=True)
files=[root/x for x in ["uuid.txt","reality_private_key.txt","reality_public_key.txt","vless_decryption.txt","vless_encryption.txt","subscription_token.txt","subscription_url.txt","subscription.txt","vless.txt","reality-sni-list.txt"]]+[config]
files=[p for p in files if p.is_file()]
if not files: raise SystemExit("no runtime state available to back up")
stamp=time.strftime("%Y%m%d-%H%M%S",time.gmtime()); tmp=backup_root/f".state-{stamp}.tmp"; out=backup_root/f"state-{stamp}.tar.gz"; manifest={}
with tarfile.open(tmp,"w:gz") as tar:
    for path in files:
        arc=Path("state")/(path.name if path.parent==root else "config.json"); tar.add(path,arcname=arc,recursive=False); manifest[str(arc)]={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"mode":oct(path.stat().st_mode&0o777)}
    info={"created_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"xray_version":os.getenv("XRAY_VERSION","unknown"),"files":manifest}
    import io; payload=json.dumps(info,sort_keys=True,indent=2).encode()+b"\n"; ti=tarfile.TarInfo("manifest.json"); ti.size=len(payload); ti.mode=0o600; tar.addfile(ti,io.BytesIO(payload))
os.chmod(tmp,0o600); os.replace(tmp,out)
archives=sorted(backup_root.glob("state-*.tar.gz"),key=lambda p:p.stat().st_mtime,reverse=True)
for old in archives[5:]:
    try: old.unlink()
    except OSError: pass
print(f"state backup created: {out.name}")
