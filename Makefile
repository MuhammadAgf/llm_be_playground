# Makefile for llm_be_playground

# Git version variables
GIT_VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev-$(shell git rev-parse --short HEAD 2>/dev/null || echo 'unknown')")
GIT_COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || echo 'unknown')
IMAGE_NAME := llm-be-playground
IMAGE_TAG := $(GIT_VERSION)

.PHONY: install run dev clean docker-build docker-run docker-stop docker-clean setup docker-compose-up docker-compose-down docker-compose-logs docker-build-latest

install:
	python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000

dev:
	. venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf venv __pycache__ .pytest_cache 

# Docker commands with git versioning
docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -t $(IMAGE_NAME):latest .

docker-build-latest:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -t $(IMAGE_NAME):latest . --no-cache

docker-run:
	docker run -d --name $(IMAGE_NAME) -p 8000:8000 $(IMAGE_NAME):$(IMAGE_TAG)

docker-run-latest:
	docker run -d --name $(IMAGE_NAME) -p 8000:8000 $(IMAGE_NAME):latest

docker-stop:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

docker-clean:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	docker rmi $(IMAGE_NAME):latest || true

# Docker Compose commands
docker-compose-up:
	GIT_VERSION=$(GIT_VERSION) docker compose up -d

docker-compose-down:
	docker compose down

docker-compose-logs:
	docker compose logs -f

docker-compose-build:
	GIT_VERSION=$(GIT_VERSION) docker compose build --no-cache

# Setup script
setup:
	chmod +x setup.sh && ./setup.sh

# Show current version info
version:
	@echo "Git Version: $(GIT_VERSION)"
	@echo "Git Commit: $(GIT_COMMIT)"
	@echo "Image Name: $(IMAGE_NAME)"
	@echo "Image Tag: $(IMAGE_TAG)" 