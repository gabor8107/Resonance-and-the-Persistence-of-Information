import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from release_summary import run
class Release(unittest.TestCase):
 def test_replayed_counts(self):
  r=run();self.assertEqual((r['rows'],r['included_cadences'],r['included_sectors']),(332028,327256,53));self.assertEqual(r['pipeline']['core']['correct']['Combined'],34);self.assertEqual(r['pipeline']['core_q25']['correct']['Combined'],38)
