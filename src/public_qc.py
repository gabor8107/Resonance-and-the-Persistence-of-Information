#!/usr/bin/env python3
"""Recompute public numerical claims from packaged, non-proprietary data.
Requires numpy, scipy. NO network, NO restricted MRIT detector code.
"""
from pathlib import Path
import csv, json, sys
import numpy as np
from scipy.stats import rankdata
ROOT=Path(__file__).resolve().parents[1]

def run():
    with (ROOT/'data/tess_s75_public_sap.csv').open(newline='') as f:rows=list(csv.DictReader(f))
    def col(name):return np.asarray([float(row[name]) if row[name] else np.nan for row in rows])
    a=col('tic_159717535_sap_flux'); b=col('tic_159717461_sap_flux')
    qa=col('tic_159717535_quality'); qb=col('tic_159717461_quality')
    mask=(qa==0)&(qb==0)&np.isfinite(a)&np.isfinite(b)
    r=float(np.corrcoef(a[mask],b[mask])[0,1]);n=int(mask.sum())
    good_b=(qb==0)&np.isfinite(b)
    missing=~np.isfinite(a[good_b]); score=b[good_b]
    # Probability that non-missing observations have higher comparison flux than missing ones.
    ranks=rankdata(score,method='average')
    n_non=(~missing).sum();n_mis=missing.sum()
    U=ranks[~missing].sum()-n_non*(n_non+1)/2
    auc=float(U/(n_non*n_mis))
    t=col('bjd_minus_2457000')
    # Simple, transparent Fourier least-squares fit with first four harmonics.
    # A fixed 1.7643 cycles/day reference (an observationally visible variation)
    # reproduces the sampling-window effect described in the public preprint.
    def harmonic_ratios(mask,flux,frequency_cpd=1.7643):
        tt=t[mask].astype(float); yy=flux[mask].astype(float)
        tt=tt-tt.mean()
        x=np.column_stack([np.ones(tt.size),tt]+[term for n in range(1,5) for term in (np.sin(2*np.pi*n*frequency_cpd*tt),np.cos(2*np.pi*n*frequency_cpd*tt))])
        beta=np.linalg.lstsq(x,yy,rcond=None)[0]
        amps=np.asarray([np.hypot(beta[2+2*j],beta[3+2*j]) for j in range(4)])
        return (amps[1:]/amps[0]).tolist()
    good_a=(qa==0)&np.isfinite(a)
    good_b=(qb==0)&np.isfinite(b)
    ra=np.asarray(harmonic_ratios(good_a,a)); rb_full=np.asarray(harmonic_ratios(good_b,b)); rb_matching=np.asarray(harmonic_ratios(mask,b))
    dist_raw=float(np.sqrt(np.mean((ra-rb_full)**2)))
    dist_common=float(np.sqrt(np.mean((ra-rb_matching)**2)))
    with (ROOT/'data/kepler_public_inventory.csv').open() as f:inventory=list(csv.DictReader(f))
    with (ROOT/'data/published_identity_loss_aggregates.csv').open() as f:agg=list(csv.DictReader(f))
    out={
      'tess':{'matched_quality0_finite_SAP_samples':n,'pearson_r':r,'missingness_auc_using_flux':auc, 'interpretation':'shared variability or contamination candidate, NOT two independent physical sources'},
      'tess_sampling_control':{'harmonic_reference_frequency_cpd':1.7643,'harmonics_used':[1,2,3,4],'tic_159717535_ratios':ra.tolist(),'tic_159717461_full_ratios':rb_full.tolist(),'tic_159717461_matched_ratios':rb_matching.tolist(),'RMS_before_matched_sampling':dist_raw,'RMS_after_matched_sampling':dist_common,'RMS_reduction_factor':float(dist_raw/dist_common)},
      'kepler_inventory':{'n_lightcurves':len(inventory),'n_rows':sum(int(z['observations']) for z in inventory)},
      'v05_published_summary_only':[{'retained_fraction':float(z['retained_fraction']),'n':int(z['n_assignments']),**{k+'_pct':round(100*int(z[k+'_correct'])/int(z['n_assignments']),4) for k in ['absolute','R','R_T','combined']}} for z in agg],
      'reproducibility_scope':'Recomputes public QC and summary metrics. Does NOT re-run undisclosed MRIT feature extraction or prove classifier performance.'
    }
    dest=ROOT/'results/public_qc.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(out,indent=2,ensure_ascii=False));return out
if __name__=='__main__':run()
