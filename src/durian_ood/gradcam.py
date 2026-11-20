"""Grad-CAM on the last feature map before global pooling (1280 x 7 x 7 for EfficientNet-B0 at 224 px)."""
import numpy as np
import torch
import torch.nn.functional as F


def gradcam(model, x, cls=None):
    """`model` is a timm classifier in eval mode, `x` a (1, 3, 224, 224) tensor.
    Returns (cam 7 x 7 array, logits, class index). The CAM is for the predicted class unless `cls` is given."""
    with torch.enable_grad():
        feats = model.forward_features(x)
        feats.retain_grad()
        logits = model.forward_head(feats)
        c = int(logits.argmax(1)) if cls is None else int(cls)
        model.zero_grad(set_to_none=True)
        logits[0, c].backward()
    w = feats.grad.mean((2, 3), keepdim=True)
    cam = F.relu((w * feats).sum(1))[0].detach().cpu().numpy()
    return cam, logits.detach().float().cpu()[0], c


def upsample(cam, size=224):
    from PIL import Image
    cam = cam / (cam.max() + 1e-8)
    return np.asarray(Image.fromarray((cam * 255).astype(np.uint8)).resize((size, size), Image.BILINEAR), np.float32) / 255
