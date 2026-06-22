"""A tiny deterministic demo model used for the portfolio gRPC service.

The class is intentionally simple and self-contained so that the repository can
be run without external training data. It mimics the shape of a binary
classifier by exposing a ``predict_proba(features)`` method.
"""
from __future__ import annotations

import math
from typing import Iterable


class SimpleModel:
    """Small deterministic binary-classification demo model."""

    def predict_proba(self, features: Iterable[float]) -> float:
        values = [float(x) for x in features]
        if not values:
            return 0.0

        # A deterministic score: enough for a service demo, not a real ML model.
        mean_value = sum(values) / len(values)
        score = 1.2 * (mean_value - 1.5)
        probability = 1.0 / (1.0 + math.exp(-score))
        return max(0.0, min(1.0, probability))
