.PHONY: install model proto server client test docker-build docker-run

install:
	pip install -r requirements.txt

model:
	python -m scripts.create_demo_model

proto:
	python -m grpc_tools.protoc -Iprotos --python_out=protos --grpc_python_out=protos protos/model.proto

server:
	python -m server.server

client:
	python -m client.client --features 1 2 3

test:
	pytest -q

docker-build:
	docker build -t ml-grpc-prediction-service .

docker-run:
	docker run --rm -p 50051:50051 -e MODEL_VERSION=v1.0.0 ml-grpc-prediction-service
