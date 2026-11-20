"""Quality-aware augmentation, applied to the 256 x 256 image before the usual training transforms.

`rand_quality` is the full augmentation (`qaug`). `rand_quality_parts` switches its three
components on and off; with all three on it returns exactly what `rand_quality` returns for
the same random generator state.
"""
import io

import numpy as np
from PIL import Image

P_DOWNSCALE = 0.6
SCALE = (0.25, 1.0)
P_JPEG = 0.6
JPEG_Q = (30, 96)          # numpy integers(): upper bound exclusive, so quality 30-95
P_NOISE = 0.3


def rand_quality(a, rng):
    if rng.random() < P_DOWNSCALE:
        s = max(16, int(256 * rng.uniform(*SCALE)))
        im = Image.fromarray(a).resize((s, s), Image.BILINEAR)
        a = np.asarray(im.resize((256, 256), rng.choice([Image.BILINEAR, Image.BICUBIC, Image.NEAREST])))
    if rng.random() < P_JPEG:
        buf = io.BytesIO()
        Image.fromarray(a).save(buf, 'JPEG', quality=int(rng.integers(*JPEG_Q)))
        a = np.asarray(Image.open(buf).convert('RGB'))
    if rng.random() < P_NOISE:
        a = np.clip(a.astype(np.float32) + rng.normal(0, rng.uniform(2, 8), a.shape), 0, 255).astype(np.uint8)
    return a


def rand_quality_parts(a, rng, parts=('resize', 'jpeg', 'noise'), p_jpeg=P_JPEG):
    if 'resize' in parts and rng.random() < P_DOWNSCALE:
        s = max(16, int(256 * rng.uniform(*SCALE)))
        im = Image.fromarray(a).resize((s, s), Image.BILINEAR)
        a = np.asarray(im.resize((256, 256), rng.choice([Image.BILINEAR, Image.BICUBIC, Image.NEAREST])))
    if 'jpeg' in parts and rng.random() < p_jpeg:
        buf = io.BytesIO()
        Image.fromarray(a).save(buf, 'JPEG', quality=int(rng.integers(*JPEG_Q)))
        a = np.asarray(Image.open(buf).convert('RGB'))
    if 'noise' in parts and rng.random() < P_NOISE:
        a = np.clip(a.astype(np.float32) + rng.normal(0, rng.uniform(2, 8), a.shape), 0, 255).astype(np.uint8)
    return a
