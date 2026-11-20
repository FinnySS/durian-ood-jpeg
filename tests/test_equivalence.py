"""The functions in src/ must give the same output as the code that produced the paper's results."""
import io
import json
import re
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image

import durian_ood as d

NB = Path(__file__).resolve().parents[1] / 'notebooks' / '14_jpeg_confirmation.ipynb'


def _notebook_function(name):
    code = '\n'.join(''.join(c['source']) for c in json.loads(NB.read_text())['cells'] if c['cell_type'] == 'code')
    m = re.search(rf'^([ \t]*)def {name}\(.*?(?=^\1(?:def |\S)|\Z)', code, re.S | re.M)
    return textwrap.dedent(m.group(0))


def _load(*names):
    ns = dict(io=io, np=np, Image=Image, JPEG_Q=70,
              Q_P_DOWNSCALE=0.6, Q_SCALE=(0.25, 1.0), Q_P_JPEG=0.6, Q_JPEG=(30, 96), Q_P_NOISE=0.3)
    for n in names:
        exec(_notebook_function(n), ns)
    return ns


def _images(n=8, seed=0):
    rng = np.random.default_rng(seed)
    base = rng.integers(0, 256, (n, 32, 32, 3), dtype=np.uint8)
    return [np.asarray(Image.fromarray(b).resize((256, 256), Image.BICUBIC)) for b in base]


def test_degrade_and_variants():
    ns = _load('jpeg', 'degrade', 'apply_variant')
    for a in _images():
        for v in d.variants():
            assert np.array_equal(d.apply_variant(a, v), ns['apply_variant'](a, v)), v
        for s in (224, 160, 112, 80):
            for q in (95, 70, 30):
                assert np.array_equal(d.degrade(a, s, q), ns['degrade'](a, s, q))


def test_quality_augmentation():
    ns = _load('rand_quality', 'rand_quality_parts')
    for i, a in enumerate(_images(16, seed=1)):
        assert np.array_equal(d.rand_quality(a, np.random.default_rng(i)), ns['rand_quality'](a, np.random.default_rng(i)))
        for parts in [('resize', 'jpeg', 'noise'), ('jpeg',), ('resize',), ('noise',)]:
            assert np.array_equal(d.rand_quality_parts(a, np.random.default_rng(i), parts),
                                  ns['rand_quality_parts'](a, np.random.default_rng(i), parts))
        assert np.array_equal(d.rand_quality_parts(a, np.random.default_rng(i)), d.rand_quality(a, np.random.default_rng(i)))


def test_decision_rules():
    p = np.array([[0.70, 0.20, 0.10], [0.10, 0.10, 0.80], [0.30, 0.25, 0.45]])
    other = 2
    assert d.accept_top1(p, other).tolist() == [True, False, False]
    assert d.accept_max_confidence(p, other).tolist() == [True, False, False]
    assert d.accept_p_other(p, other, tau=0.5).tolist() == [True, False, True]
