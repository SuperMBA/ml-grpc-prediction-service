# Architecture

```text
client/client.py
      |
      | gRPC request: Health / Predict
      v
server/server.py
      |
      | loads demo model from models/model.pkl
      v
server/simple_model.py
```

## Components

- **Protocol Buffers** define the service contract in `protos/model.proto`.
- **gRPC server** exposes `Health` and `Predict` methods.
- **Client** sends a feature vector and prints prediction, confidence and model version.
- **Dockerfile** packages the server for containerized execution.
- **Environment variables** control port, model path and model version.

## Why this project is useful for portfolio review

This project demonstrates backend service design around an ML model, not just notebook-based analysis. It shows a small but complete service boundary: API contract, server implementation, client implementation, model loading, error handling and containerization.
