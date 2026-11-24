"""Recompute published accuracy from released binary outcome ledger (not a classifier)."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
METHODS=['Absolute','R','R+T','Combined']
def run():
 with (ROOT/'data/sector_outcomes.csv').open() as f: rows=list(csv.DictReader(f))
 with (ROOT/'data/pixel_inventory.csv').open() as f: inv=list(csv.DictReader(f))
 assert len({(r['kic'],r['sector']) for r in inv})==len(inv)==54
 out={'sectors':len(inv),'rows':sum(int(r['rows']) for r in inv),'included_sectors':sum(int(r['included']) for r in inv),'included_cadences':sum(int(r['quality_finite']) for r in inv if int(r['included'])),'pipeline':{}}
 for p in sorted({r['pipeline'] for r in rows}):
  a=[r for r in rows if r['pipeline']==p]; assert len(a)==len({(r['kic'],r['sector']) for r in a})==53
  out['pipeline'][p]={'n':len(a),'negative_median':sum(int(r['negative_median']) for r in a),'correct':{m:sum(int(r[m+'_correct']) for r in a) for m in METHODS},'per_target':{k:{m:sum(int(r[m+'_correct']) for r in a if r['kic']==k) for m in METHODS} for k in sorted({r['kic'] for r in a})}}
 (ROOT/'results/release_summary.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2));return out
if __name__=='__main__':run()
