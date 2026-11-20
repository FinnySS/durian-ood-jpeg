"""Compression stress test (paper, Eq. 4).

A copy at level s is made from the 256 x 256 image by reducing it to s x s (bilinear),
saving it as JPEG and enlarging it back to 256 x 256 (bicubic). The network then applies
its usual 224 x 224 input transform. Every level is made from the original, not from the
previous level.
"""
import io

import numpy as np
from PIL import Image

LEVELS = (224, 160, 112, 80)
JPEG_QUALITY = 70


def jpeg(im, q):
    b = io.BytesIO()
    im.save(b, 'JPEG', quality=int(q))
    b.seek(0)
    return Image.open(b).convert('RGB')


def degrade(a, s=160, q=70):
    im = Image.fromarray(a).resize((s, s), Image.BILINEAR)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q)
    return np.asarray(Image.open(buf).convert('RGB').resize((256, 256), Image.BICUBIC))


def standard_levels(levels=LEVELS):
    return ['original'] + [f'{s}px' for s in levels]


def variants(levels=LEVELS):
    """Standard levels plus the controls that separate JPEG from resizing."""
    return standard_levels(levels) + ['jpeg_only'] + [f'{s}px_nojpeg' for s in levels[1:]]


def apply_variant(a, name, q=JPEG_QUALITY):
    """`a` is a uint8 256 x 256 x 3 array. Names: original, <s>px, jpeg_only, <s>px_nojpeg."""
    a = np.asarray(a)
    if name == 'original':
        return a
    if name == 'jpeg_only':
        return np.asarray(jpeg(Image.fromarray(a), q))
    s = int(name.split('px')[0])
    if name.endswith('_nojpeg'):
        return np.asarray(Image.fromarray(a).resize((s, s), Image.BILINEAR).resize((256, 256), Image.BICUBIC))
    return degrade(a, s, q)
