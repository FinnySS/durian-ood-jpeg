# Results

Summary files written by the notebooks on Kaggle (Tesla T4). They are the files the paper's numbers come from. Per-image probabilities, checkpoints and image caches are not included.

| Folder | Notebook | Key files |
|---|---|---|
| `13_control_quality_matching/` | control experiment (resolution matching) | `causal_verdict.csv`, `causal_summary.csv`, `matching_check.csv`, `quality_by_source.csv` |
| `14_jpeg_confirmation/` | confirmation experiment (JPEG vs resize vs noise) | `preregistration.json`, `jpeg14_verdict.json`, `jpeg14_summary.csv`, `grid_summary.csv`, `field_jpeg_vs_resize.csv` |
| `22_jpeg_three_architectures/` | component test in MobileNetV3-Large and MobileNetV4-Conv-S | `preregistration.json`, `verdict22.json`, `fig4_values.csv`, `*_verdict_table.csv` |

Rates are percentages. `other_as_disease` is the share of the 77 out-of-scope test images assigned to a disease class under the top-1 rule; `disease_as_other` is the reverse error on the 811 in-scope test images. Intervals are 95% cluster-bootstrap intervals over image groups (2000 resamples).

## Verdicts

| Experiment | Verdict | Detail |
|---|---|---|
| 13, resolution matching (P2) | not met | `match_other` closed 6% of the gap at 112 px (criterion ≥ 50%) |
| 14, primary (H-JPEG) | confirmed | `qaug_jpeg` 103%, `qaug_resize` 11%, `qaug_noise` 6% of the gap |
| 14, S1 reversal | met (narrowly) | |
| 14, S2 JPEG on disease images only | met | |
| 14, S3 orchard photographs | met | |
| 14, S4 dose-response | not met | quality 95 already added 12.6 points (limit 10) |
| 22, MobileNetV3-Large | confirmed | `qaug_jpeg` 86%, `qaug_resize` −38% |
| 22, MobileNetV4-Conv-S | not confirmed | `qaug_jpeg` 77% (criterion ≥ 80%), `qaug_resize` −40% |

## Language of the verdict files

The verdict JSON files are kept exactly as the runs wrote them, and the notebooks at the time printed verdicts in Thai. The notebooks in this repository now print English. Translation of the recorded values:

| Recorded | English |
|---|---|
| ยืนยัน | confirmed |
| ไม่ยืนยัน | not confirmed |
| ผ่าน / ไม่ผ่าน | met / not met |
| เสร็จ | done |
| ยืนยัน 1 จาก 2 สถาปัตยกรรม (รายงานตามจริง) | confirmed in 1 of 2 architectures |
| ภาพโรคมีร่องรอยบล็อกมากกว่า other (สอดคล้องกับคำอธิบาย ก) | disease images carry more block artefacts than other (consistent with explanation a) |

`preregistration.json` holds the criteria with the time they were recorded, before any model of that experiment was trained. The criteria in the notebooks are unchanged; the notebooks stop if they differ from this record.

In notebook 22, seed 2 of `base` (both architectures) and of `qaug` (MobileNetV4-Conv-S) were retrained because the original checkpoints were not available; `runs22.csv` lists the source of every run.
