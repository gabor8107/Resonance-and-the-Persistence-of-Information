# Resonance and the Persistence of Information

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24509694.svg)](https://doi.org/10.5281/zenodo.24509694)

*An Exploratory Framework for Source Identity, Pattern Recognition and Information Loss in Oscillatory Systems*

P. Gabor | Independent researcher, Hungary | Research release v0.5 | 24 November 2026

Exploratory preprint, not peer reviewed. Previous method name: MRIT. No claim of new force, intelligence, universal resonance law or classifier superiority.

## Run
```bash
python -m pip install -r requirements.txt
python src/public_qc.py
python src/release_summary.py
python -m unittest discover -s tests -v
```
Optional raw FITS inventory: `python src/verify_cutouts.py /path/to/original/cutout_zips`. The exact filenames and SHA-256 are in `data/cutout_manifest.csv`.

## Evidence and boundaries
- Historical QLP sector 75 QC: paired flux correlation and sampling-window discrepancy.
- Five Kepler reference targets, 54 TESS sectors, 53 included, 332,028 input rows and 327,256 included cadences. Core aperture: absolute 37/53, R 15/53, R+T 15/53, combined 34/53. Alternative outer lower-quartile background: 39/53, 18/53, 18/53, 38/53.
- Repeated sectors are not independent stars. Target labels are based on requested coordinates, not proven flux purity. All five requested positions agree with catalogue coordinates; see provenance.
- Public scripts reproduce QC and reported ledger arithmetic. The private frozen classifier, calibration, distances, full historical records and communication protocol are **not** released. Public code cannot independently regenerate classifier predictions.
- Raw Kepler/TESS inputs are not redistributed in this ZIP; see provenance. No general open-source license is granted without author approval.

Read the current PDF in `docs/`. This repository is prepared for upload; nothing has been uploaded.
