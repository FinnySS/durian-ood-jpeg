import numpy as np
import torch


def fit_temperature(logits, y):
    """Temperature scaling on validation logits (L-BFGS on log T)."""
    logT = torch.zeros(1, requires_grad=True)
    opt = torch.optim.LBFGS([logT], lr=0.1, max_iter=200)
    yt = torch.as_tensor(y)

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.cross_entropy(logits / logT.exp(), yt)
        loss.backward()
        return loss

    opt.step(closure)
    return float(logT.detach().exp())


def ece(probs, y, n_bins=15):
    conf, pred = probs.max(1), probs.argmax(1)
    acc = pred == y
    e = 0.0
    edges = np.linspace(0, 1, n_bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs(acc[m].mean() - conf[m].mean())
    return float(e)
