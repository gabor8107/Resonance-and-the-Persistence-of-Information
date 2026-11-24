import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from public_qc import run
class CheckPublicQC(unittest.TestCase):
 def test_science_values(self):
  x=run();self.assertEqual(x['tess']['matched_quality0_finite_SAP_samples'],6205)
  self.assertAlmostEqual(x['tess']['pearson_r'],0.9969551455,places=6)
  self.assertAlmostEqual(x['tess']['missingness_auc_using_flux'],0.9995829606,places=5)
  self.assertAlmostEqual(x['tess_sampling_control']['RMS_before_matched_sampling'],0.22951,places=4)
  self.assertAlmostEqual(x['tess_sampling_control']['RMS_after_matched_sampling'],0.00531,places=4)
  self.assertEqual(x['kepler_inventory']['n_rows'],895400)
  self.assertEqual(len(x['v05_published_summary_only']),4)
if __name__=='__main__':unittest.main()
