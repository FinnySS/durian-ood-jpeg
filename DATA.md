# Data

**No images, image caches or model weights are distributed in this repository.**
Download each public dataset from its original source and respect its licence.

## 1. Datasets used

| Dataset | Images used | Role | Licence | Source |
|---|---:|---|---|---|
| Vinh Long durian leaf, stem and fruit dataset (Nguyen, 2025) | 5,451 | 10 in-scope classes | CC BY 4.0 | *Data in Brief* 63, 112244 · doi:[10.17632/mhjwyb5p48.1](https://doi.org/10.17632/mhjwyb5p48.1) |
| iNaturalist observations (10 non-durian plant taxa × 40, plus animals and fungi) | 480 | out-of-scope class `other` | per photo, **mostly CC BY-NC** | [inaturalist.org](https://www.inaturalist.org) |
| TACO, ground-level images (Proença & Simões, 2020) | 80 | `other` | see dataset | arXiv:2003.06975 |
| Synthetic blurred, dark and over-exposed images | 40 | `other` | generated | — |
| DurianLDD | see paper | second in-scope dataset (replication) | see dataset | see paper reference list |
| Orchard photographs, Ranong Province, Thailand | 59 (O1) + 124 (O2) non-durian | field test | **not released** | collected by the authors |

In-scope classes (alphabetical, as in `classes.json`): anthracnose_disease, canker_disease, fruit_rot, mealybug_infestation, **other**, pink_disease, sooty_mold, stem_blight, stem_cracking_gummosis, thrips_disease, yellow_leaf.

## 2. Why some data are not released

* **iNaturalist photos** are mostly licensed for non-commercial use with attribution. We cannot redistribute them in a code repository, and models trained on them inherit this restriction. The attribution list (photo IDs, observers and licences) is available on request, so the class can be rebuilt.
* **Orchard photographs** were taken on private farms. They are not released, to protect the privacy of growers and staff, except the single example image below. Orchards are referred to by codes only (O1, O2).
* **Trained weights** are not released because their training data include non-commercial images.

## 3. Expected input files

The notebooks in this repository start from three files, uploaded as a private Kaggle dataset or placed under one folder on Google Drive:

* `cache256.npy`: every image resized to 256 x 256, uint8, shape (6051, 256, 256, 3), about 1.2 GB
* `metadata.csv`: one row per image with at least `label`, `split` (train / val / test) and `group`, in the row order of the cache
* `classes.json`: class names in index order

The cache was built from RGB copies of the images with the long side capped at 1024 px and EXIF removed. The audit and splitting notebooks that produce these files are available from the authors on request.

## 4. Split

Near-duplicates and sequential shots are grouped before splitting: perceptual hash (Hamming distance ≤ 6) and DINOv2 ViT-S/14 embeddings (average linkage, cosine similarity 0.87) within each class, merged with union-find (2,696 groups). A stratified group split then gives **4,304 train / 859 validation / 888 test** images (77 out-of-scope test images). The grouping is a proxy for capture sessions and still leaks; see the paper for the leakage analysis. A random split with the same proportions is stored in `split_random` for comparison.

## 5. Audit notes on the public dataset

* Every file carries XMP metadata reading `Screenshot`, consistent with screen captures; no capture times or camera metadata are present.
* 5,451 images form 2,109 proxy groups (2.58 images per group on average).
* 177 JPEG files are 224 × 224 px and 534 PNG files are low-resolution.
* Some images contain watermarks, white borders or video frames.

These properties are reported as observations, not as errors in the dataset.

## 6. Example image

`examples/orchard_nondurian.jpg` is one non-durian photograph from orchard O2 (leaf litter, irrigation hoses and grass; no people or landmarks). It is the photograph shown in the paper's stress-test figure and is used by `notebooks/example_stress_test.ipynb`.
