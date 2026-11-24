"""MRIT independent input-file verification; archival audit, not an MRIT detection claim.
Run with: python src/independent_audit.py --root /path/to/repo
No proprietary engine required. Requires numpy and scipy only for rank/statistics.
"""
import argparse, csv, hashlib, json, re, tarfile, zipfile
from pathlib import Path
import numpy as np

def fits_hdu(data, start):
    pos=start; meta={}
    while True:
        card=data[pos:pos+80].decode('ascii','replace'); pos+=80
        key=card[:8].strip()
        if card[8:10]=='= ':
            raw=card[10:80].split('/')[0].strip()
            try: val=float(raw) if any(c in raw for c in '.Ee') else int(raw)
            except: val=raw.strip(" '")
            meta[key]=val
        if key=='END':break
    return meta,((pos+2879)//2880)*2880

def tess_table(blob):
    h,p=fits_hdu(blob,0); h1,p1=fits_hdu(blob,p)
    kinds={'E':'>f4','D':'>f8','J':'>i4','I':'>i2','B':'u1','K':'>i8'}
    dtype=[]
    for j in range(1,int(h1['TFIELDS'])+1):
        k=str(h1['TTYPE'+str(j)]); fmt=str(h1['TFORM'+str(j)])
        m=re.fullmatch(r'(\d*)([EDJIBKA])',fmt)
        if not m: raise ValueError('Unexpected FITS column '+k+' '+fmt)
        n=int(m.group(1) or '1'); d=kinds.get(m.group(2),"S1")
        dtype.append((k,d,(n,)) if n>1 else (k,d))
    dt=np.dtype(dtype)
    if dt.itemsize!=h1['NAXIS1']:raise ValueError('FITS row length mismatch')
    return h, np.frombuffer(blob,dtype=dt,count=h1['NAXIS2'],offset=p1).copy()

