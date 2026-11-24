"""Optional independent input inventory check. Supply the original five TESSCut ZIPs."""
import csv,hashlib,sys,zipfile
from pathlib import Path
import numpy as np
from fits_table import tess_table
ROOT=Path(__file__).resolve().parents[1]
def main(folder):
 with (ROOT/'data/cutout_manifest.csv').open() as f: manifest=list(csv.DictReader(f))
 with (ROOT/'data/pixel_inventory.csv').open() as f: expected={(r['kic'],int(r['sector'])):r for r in csv.DictReader(f)}
 checked=set()
 for r in manifest:
  p=folder/r['archive']; assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
  with zipfile.ZipFile(p) as z:
   for n in z.namelist():
    if not n.endswith('.fits'): continue
    h,d=tess_table(z.read(n)); k=(r['kic'],int(h['SECTOR'])); ref=expected[k]
    F=np.asarray(d['FLUX'],float).reshape(-1,64); ok=(d['QUALITY']==0)&np.isfinite(d['TIME'])&np.isfinite(F).all(axis=1)
    assert len(d)==int(ref['rows']) and ok.sum()==int(ref['quality_finite']),k
    checked.add(k)
 assert checked==set(expected);print('Verified 54 source/sector inventory records and all five archive hashes.')
if __name__=='__main__':main(Path(sys.argv[1]))
