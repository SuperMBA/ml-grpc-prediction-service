from __future__ import annotations

import argparse
import os

import grpc

from protos import model_pb2, model_pb2_grpc

DEFAULT_GRPC_ADDRESS = os.environ.get("GRPC_ADDRESS", "localhost:50051")


def call_health(stub: model_pb2_grpc.PredictionServiceStub) -> None:
    response = stub.Health(model_pb2.HealthRequest())
    print("Health response:")
    print(f"  status: {response.status}")
    print(f"  modelVersion: {response.modelVersion}")


def call_predict(stub: model_pb2_grpc.PredictionServiceStub, features: list[float]) -> None:
    response = stub.Predict(model_pb2.PredictRequest(features=features))
    print("Predict response:")
    print(f"  prediction: {response.prediction}")
    print(f"  confidence: {response.confidence:.4f}")
    print(f"  modelVersion: {response.modelVersion}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Client for the ML gRPC prediction service")
    parser.add_argument("--address", default=DEFAULT_GRPC_ADDRESS, help="gRPC server address")
    parser.add_argument("--features", nargs="+", type=float, default=[1.0, 2.0, 3.0])
    args = parser.parse_args()

    with grpc.insecure_channel(args.address) as channel:
        stub = model_pb2_grpc.PredictionServiceStub(channel)
        print("=== /health ===")
        call_health(stub)
        print("\n=== /predict ===")
        call_predict(stub, args.features)


if __name__ == "__main__":
    main()
