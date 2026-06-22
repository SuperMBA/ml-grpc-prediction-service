# ML gRPC Prediction Service

A compact Python backend project that exposes a demo machine-learning model through a typed **gRPC API**.

This repository demonstrates how an ML model can be served as a backend service with a clear API contract, health endpoint, prediction endpoint, model versioning and Docker-based deployment.

## Why this project matters

Most ML portfolio projects are notebooks. This project shows a more production-oriented pattern: a model is wrapped behind a service boundary and accessed through a client/server API.

It is useful for roles involving:

- Python backend development
- ML model serving
- API integrations
- AI/ML platform engineering basics
- MLOps-oriented workflows
- AI code review / AI trainer projects involving backend logic

## Features

- gRPC service defined with Protocol Buffers
- `Health` endpoint for service/model status
- `Predict` endpoint for feature-vector prediction
- Python server implementation
- Python client implementation
- Demo model loading from `models/model.pkl`
- Safe fallback demo model if the pickle cannot be loaded
- Environment-based configuration
- Dockerfile for containerized execution
- Basic tests for model behavior

## Project structure

```text
ml-grpc-prediction-service/
├── client/
│   └── client.py
├── docs/
│   ├── architecture.md
│   └── portfolio_description.md
├── models/
│   └── model.pkl
├── protos/
│   ├── model.proto
│   ├── model_pb2.py
│   └── model_pb2_grpc.py
├── scripts/
│   └── create_demo_model.py
├── server/
│   ├── server.py
│   └── simple_model.py
├── tests/
│   └── test_simple_model.py
├── Dockerfile
├── Makefile
├── requirements.txt
└── .env.example
```

## API contract

The service is defined in `protos/model.proto`.

```proto
service PredictionService {
  rpc Health(HealthRequest) returns (HealthResponse) {}
  rpc Predict(PredictRequest) returns (PredictResponse) {}
}
```

### Health response

```text
status: ok
modelVersion: v1.0.0
```

### Predict response

```text
prediction: 1
confidence: 0.6457
modelVersion: v1.0.0
```

## Run locally

### 1. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create demo model

```bash
python -m scripts.create_demo_model
```

### 4. Start the server

```bash
python -m server.server
```

### 5. Run the client in a second terminal

```bash
python -m client.client --features 1 2 3
```

## Run with Docker

Build the image:

```bash
docker build -t ml-grpc-prediction-service .
```

Run the container:

```bash
docker run --rm -p 50051:50051 -e MODEL_VERSION=v1.0.0 ml-grpc-prediction-service
```

Run the client locally:

```bash
python -m client.client --features 1 2 3
```

## Configuration

The service can be configured with environment variables:

| Variable | Default | Description |
|---|---:|---|
| `PORT` | `50051` | gRPC server port |
| `MODEL_VERSION` | `v1.0.0` | Model version returned by API |
| `MODEL_PATH` | `models/model.pkl` | Path to pickled demo model |
| `GRPC_ADDRESS` | `localhost:50051` | Client target address |

See `.env.example` for a safe example configuration.

## Tests

```bash
pytest -q
```

## Portfolio note

This is a compact service-design project. The model itself is intentionally simple; the focus is on the **ML service boundary**: Protocol Buffers contract, server implementation, client request flow, model loading, error handling, versioning and Docker packaging.

## CV bullet

**ML gRPC Prediction Service** — Python gRPC backend exposing health and prediction endpoints for a demo ML model, with Protocol Buffers contract, client/server implementation, Docker packaging, model versioning and environment-based configuration.
