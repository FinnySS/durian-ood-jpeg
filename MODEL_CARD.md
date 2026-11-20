# Model card: durian symptom classifier with a reject class

> Research model. **Weights are not released.** This card documents the models evaluated in the paper.

## Model details

* **Architecture:** EfficientNet-B0 (`efficientnet_b0.ra_in1k`, timm, ImageNet pretrained). Also evaluated: MobileNetV3-Large and MobileNetV4-Conv-S, and four further architectures in a benchmark.
* **Output:** 11 classes — 10 durian disease and pest classes plus `other` (out of scope).
* **Input:** RGB photograph. Preprocessing: EXIF rotation, long side ≤ 1024 px (Lanczos), 256 × 256 (bicubic), 224 × 224 (bilinear), ImageNet normalisation.
* **Training:** AdamW (lr 1e-3, weight decay 0.05), OneCycle schedule, class-weighted cross-entropy with label smoothing 0.1, batch 64, 30 epochs with early stopping (patience 8), dropout 0.2, three seeds (42, 1, 2).
* **Variants:** `base` (standard augmentation) and `qaug` (adds random down-and-up resizing, JPEG quality 30–95 and Gaussian noise to every class). Component variants `qaug_jpeg` and `qaug_resize` were trained for the causal experiments.
* **Calibration:** temperature scaling fitted on the validation set.
* **Deployment:** ONNX Runtime on CPU, FP32 (simple static INT8 quantisation degraded accuracy and is not used).

## Intended use

* Decision support for durian growers: suggest which known symptom a **close-up** photograph most resembles, or decline to answer.
* Research on out-of-scope rejection under image compression.

## Out-of-scope uses

* Not a diagnosis. It does not replace a plant pathologist or an extension officer.
* Not for crops other than durian, for whole-tree or distant photographs, or for diseases outside the ten classes.
* The `other` class means "unlike the close-up symptom photographs of the training data", **not** "not durian" or "healthy". There is no healthy class.

## Evaluation (EfficientNet-B0, mean of three seeds, public test set)

| Measure | `base` | `qaug` |
|---|---:|---:|
| Accuracy, original images | 96.1% | 96.6% |
| Out-of-scope images labelled as diseased, original images (top-1 rule) | 0.9% | 1.3% |
| Same, 112 px + JPEG quality 70 | 42.9% | 9.5% |
| Same, 80 px + JPEG quality 70 | 65.4% | 14.7% |

* AUROC for durian versus out-of-scope stays about 0.99 at 112 px for `base`; it does **not** reveal the failure above.
* Rejecting images whose out-of-scope probability exceeds a validation-set threshold lowered the 112-px rate to 5.6% (`base`), or 1.3% with JPEG augmentation, at a cost of about 5% of clean in-scope images rejected.
* Field (non-durian photographs, two orchards, original quality): `qaug` rejected 57 of 59 on O1 (seed 42) and 99.7% on O2 (mean of three seeds).

Full results, intervals and pre-specified criteria are in the paper and `results/`.

## Known failure modes

* **Small JPEG-compressed images** (small photos, thumbnails, tight crops of compressed photos) of non-durian scenes can be labelled as a disease. JPEG augmentation reduces but does not remove this, especially at 80 px.
* **Look-alikes.** Lichen-like patches on the bark of other trees were labelled *pink disease* with high confidence.
* **Distribution shift.** Training images are close-ups from one Vietnamese dataset. Mid-distance or whole-tree photographs from Thai orchards are mostly assigned to `other`.

## Limitations

* One main training dataset, with labels not checked by a plant pathologist; the group-aware split still leaks, so accuracy figures are upper bounds.
* 77 out-of-scope test images: one image changes a rate by 1.3 points.
* Decision thresholds were fitted on public validation images and have not been validated on field photographs of real symptoms.

## Ethical and licensing considerations

* Most out-of-scope training images are licensed non-commercial, so the trained weights cannot be used commercially and are not released.
* Orchard photographs are private and are not released. User photographs in the app are stored only with consent and without EXIF or GPS data.
* Wrong answers can lead to unnecessary or missed treatment. The app shows top-3 answers, marks uncertain answers and asks for a closer photograph instead of guessing.
