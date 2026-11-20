# Figure scripts

Scripts for the paper figures whose inputs are public. They use the paper's typography (Palatino via `mathpazo`), so they need `pdflatex` with `mathpazo` and `lmodern`. Run them from this folder; PDFs are written to `out/`.

| Script | Figure | Input |
|---|---|---|
| `ablation.py` | other→disease by stress level for `base`, `qaug`, `qaug_jpeg`, `qaug_resize` in three architectures | `components.json` (EfficientNet-B0 from notebook 14, the two MobileNets from notebook 22) |
| `jpeg_grid.py` | size × JPEG-quality grid | `../results/14_jpeg_confirmation/grid_summary.csv` |
| `quality_by_source.py` | effective resolution of disease and out-of-scope images | `quality.json` (curves from notebook 13) |

The stress-test example, the field look-alike panels and the probability histograms are built from orchard photographs or per-image probabilities that are not released, so their scripts are not included.
