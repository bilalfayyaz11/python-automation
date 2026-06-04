# Containerized API and Worker Platform

## What This Does

This system containerizes a multi-service Python application using Docker. It includes a Flask API service for receiving task requests, a Redis queue for storing asynchronous jobs, and a background worker service for processing queued tasks.

The platform demonstrates how API and worker services can be packaged into reproducible Docker images, connected through a private container network, and configured through environment variables. This pattern is commonly used in production systems where user-facing requests need to trigger background processing without blocking the API.

## Architecture

+-----------------------------+
|        Client / Curl        |
+--------------+--------------+
               |
               v
+-----------------------------+
|       Flask API Container   |
|       Port: 5000            |
|       Image: task-api:v1    |
+--------------+--------------+
               |
               v
+-----------------------------+
|       Redis Container       |
|       Queue: task_queue     |
|       Image: redis:7-alpine |
+--------------+--------------+
               |
               v
+-----------------------------+
|     Python Worker Container |
|     Image: task-worker:v1   |
|     Stores task results     |
+--------------+--------------+
               |
               v
+-----------------------------+
|       Redis Result Keys     |
|       result:<task_id>      |
+-----------------------------+

## Prerequisites

- Ubuntu Linux
- Docker Engine
- Git
- Curl
- Basic Linux shell access
- Internet access for pulling base images

## Setup & Installation

sudo apt update

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker $USER

newgrp docker

docker --version

## How to Reproduce

1. Clone this repository.

2. Enter the implementation directory.

   cd containerized-task-platform

3. Build the API image.

   docker build -t task-api:v1 -f api/Dockerfile .

4. Build the worker image.

   docker build -t task-worker:v1 -f worker/Dockerfile .

5. Create the application network.

   docker network create app-network

6. Start Redis.

   docker run -d --name redis --network app-network -p 6379:6379 redis:7-alpine

7. Start the API container.

   docker run -d --name api --network app-network -p 5000:5000 -e REDIS_HOST=redis -e REDIS_PORT=6379 task-api:v1

8. Start the worker container.

   docker run -d --name worker --network app-network -e REDIS_HOST=redis -e REDIS_PORT=6379 task-worker:v1

9. Test the API health endpoint.

   curl http://localhost:5000/health

10. Submit a task.

   curl -X POST http://localhost:5000/task -H "Content-Type: application/json" -d '{"task_type":"process","data":{"value":42}}'

11. Retrieve the task result using the returned task_id.

   curl http://localhost:5000/result/<task_id>

12. Clean up resources.

   docker stop api worker redis
   docker rm api worker redis
   docker network rm app-network
   docker rmi task-api:v1 task-worker:v1

## Tools Used

- Docker
- Python 3.11
- Flask
- Redis
- Redis Python Client
- Linux
- Curl
- Git
- Docker Bridge Networking
- Environment Variables

## Key Skills Demonstrated

- Multi-container application deployment
- Docker image creation and tagging
- API containerization
- Worker service containerization
- Redis-backed asynchronous task processing
- Container networking
- Runtime configuration through environment variables
- Service log inspection and troubleshooting
- Production-style API and background processing architecture

## Real-World Use Case

This architecture is used in companies that need APIs to trigger work that should run in the background. Examples include invoice generation, email sending, report processing, file conversion, AI inference jobs, webhook handling, fraud checks, and data pipeline triggers. Separating the API from the worker improves reliability because the API can respond quickly while background services process heavier workloads independently.

## Lessons Learned

- API and worker services should be separated when background processing is required.
- Docker networks allow containers to communicate by service/container name.
- Environment variables make containers reusable across development, staging, and production.
- Redis can act as a lightweight queue for asynchronous task processing.
- Container logs are essential for debugging service startup and task execution issues.

## Troubleshooting Log

- Completed missing TODO logic in the shared configuration, API service, and worker service.
- Added UUID-based task identifiers so submitted tasks can be tracked reliably.
- Added Redis queue push and blocking pop behavior for asynchronous processing.
- Used container names over localhost for service-to-service Redis communication.
- Removed the obsolete Docker Compose version field to avoid modern Compose warnings.
- Corrected result lookup by using the actual returned task_id instead of the literal placeholder.
