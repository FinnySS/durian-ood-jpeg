"""Decision rules on calibrated class probabilities (paper, Eqs. 9-11).

`probs` has shape (n, K); `other` is the column index of the out-of-scope class.
Each function returns a boolean array: True where the image is accepted, that is, given a
diagnosis. An accepted image is assigned the in-scope class with the highest probability.
"""
import numpy as np


def _in_scope_max(probs, other):
    p = np.array(probs, dtype=float, copy=True)
    p[:, other] = -np.inf
    return p.max(1), p.argmax(1)


def accept_top1(probs, other):
    return np.asarray(probs).argmax(1) != other


def accept_max_confidence(probs, other, threshold=0.60):
    q, _ = _in_scope_max(probs, other)
    return q >= threshold


def accept_p_other(probs, other, tau):
    return np.asarray(probs)[:, other] <= tau


def fit_tau(val_probs, val_y, other, quantile=0.95):
    """tau = 95th percentile of p(other) over in-scope validation images at original quality,
    so that about 5% of clean in-scope images are rejected. Never fit on test data."""
    val_probs, val_y = np.asarray(val_probs), np.asarray(val_y)
    return float(np.quantile(val_probs[val_y != other, other], quantile))


def predicted_class(probs, other):
    _, c = _in_scope_max(probs, other)
    return c
