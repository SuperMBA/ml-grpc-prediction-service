from __future__ import annotations

import logging
import math
import os
import pickle
from concurrent import futures
from pathlib import Path
from typing import Iterable

import grpc

from protos import model_pb2, model_pb2_grpc
from server.simple_model import SimpleModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", "50051"))
MODEL_VERSION = os.environ.get("MODEL_VERSION", "v1.0.0")
DEFAULT_MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.pkl"
MODEL_PATH = Path(os.environ.get("MODEL_PATH", str(DEFAULT_MODEL_PATH)))


def _validate_features(features: Iterable[float]) -> list[float]:
    values = [float(x) for x in features]
    if not values:
        raise ValueError("features must not be empty")
    if any(not math.isfinite(x) for x in values):
        raise ValueError("features must contain only finite numeric values")
    return values


class PredictionServiceServicer(model_pb2_grpc.PredictionServiceServicer):
    """gRPC service exposing health and prediction methods."""

    def __init__(self) -> None:
        self.model = self._load_model()

    def _load_model(self):
        """Load a pickled model, falling back to a deterministic demo model."""
        if MODEL_PATH.exists():
            try:
                with MODEL_PATH.open("rb") as f:
                    model = pickle.load(f)
                logger.info("Model loaded from %s", MODEL_PATH)
                return model
            except Exception as exc:  # pragma: no cover - defensive fallback
                logger.warning("Failed to load model from %s: %s", MODEL_PATH, exc)

        logger.info("Using built-in SimpleModel fallback")
        return SimpleModel()

    def Health(self, request, context):
        """Return service status and model version."""
        status = "ok" if self.model is not None else "model_not_loaded"
        return model_pb2.HealthResponse(status=status, modelVersion=MODEL_VERSION)

    def Predict(self, request, context):
        """Return a binary prediction and confidence for the input features."""
        try:
            features = _validate_features(request.features)
        except ValueError as exc:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(exc))
            return model_pb2.PredictResponse()

        try:
            confidence = float(self.model.predict_proba(features))
        except Exception as exc:  # pragma: no cover - defensive error handling
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Prediction failed: {exc}")
            return model_pb2.PredictResponse()

        prediction = "1" if confidence >= 0.5 else "0"
        return model_pb2.PredictResponse(
            prediction=prediction,
            confidence=confidence,
            modelVersion=MODEL_VERSION,
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServiceServicer(),
        server,
    )
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    logger.info("gRPC server started on port %s", PORT)
    logger.info("Model version: %s", MODEL_VERSION)
    logger.info("Model path: %s", MODEL_PATH)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
