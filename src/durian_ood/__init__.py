"""Reusable parts of the study: stress test, quality-aware augmentation, decision rules, calibration, Grad-CAM."""
from .stress_test import jpeg, degrade, apply_variant, standard_levels, variants
from .quality_aug import rand_quality, rand_quality_parts
from .decision_rules import accept_top1, accept_max_confidence, accept_p_other, fit_tau
from .calibration import fit_temperature, ece

__all__ = ['jpeg', 'degrade', 'apply_variant', 'standard_levels', 'variants',
           'rand_quality', 'rand_quality_parts',
           'accept_top1', 'accept_max_confidence', 'accept_p_other', 'fit_tau',
           'fit_temperature', 'ece']
