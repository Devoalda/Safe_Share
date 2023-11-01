# Safe Share

## Installation

```bash
# Clone the repository
python -m venv venv

## On linux
source venv/bin/activate

## On Windows
venv\Scripts\activate

cd safeshare
pip install -r requirements.txt
```

## Usage

### Running Backend & Frontend Together (Using Docker Compose)

A sample docker compose file is provided in the root directory. You can use it to run the backend and frontend together.

> Please modify the environment variables in the docker-compose.yml file before running it.
 
APIs:
- [VirusTotal](https://developers.virustotal.com/v3.0/reference)
- [AWS DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS](https://aws.amazon.com/)

```bash
# Run backend & frontend using docker-compose
docker-compose up
```

### Running Backend & Frontend Separately (Docker + Kubernetes)
```bash
# Run frontend using docker-compose
docker compose -f  docker-compose-frontend.yml up -d

# Run backend using kubernetes
cd K8s
kubectl apply -f redis_deployment.yaml
kubectl apply -f backend_deployment.yaml
kubectl apply -f backend_service.yaml
```
### For development

Copy the `env` file to `.env` and modify the environment variables accordingly.

```bash
# Run frontend locally
cd ../safeshare-frontend
npm install
npm start

# Run backend locally (After installing requirements.txt)
cd ../safeshare
python manage.py runserver
```

## Endpoints

> React App - `http://localhost:3000/` (if running locally)

> Django App - `http://localhost:8000/` (if running locally)

> React App - `http://localhost:80/` (if running using docker-compose)

- `Django App` - `http://localhost:8000/api/` - Django REST API

## Python Testing Scripts

>DO NOT MISUSE THESE SCRIPTS. THEY ARE FOR TESTING PURPOSES ONLY

```bash
# All scripts are in saveshare_app/

# post_and_get_files.py
# Uploads a file to the server and then downloads it
python post_and_get_files.py

# stressTest.py
# Uploads multiple files in multiple threads (upload/download)
python stressTest.py
```

## Features

## React App

Frontend is built using ReactJS and TailwindCSS. It is Containerised using Docker.

An image is here [amusement3004/safeshare-frontend:latest](https://hub.docker.com/repository/docker/amusement3004/safeshare-frontend)

## Django App

Backend is built using Django REST Framework. It is Containerised using Docker.

An image is here [amusement3004/safeshare:latest](https://hub.docker.com/repository/docker/amusement3004/safeshare)

## Virus Scanning Microservice

Virus Scanning microservice is built using [gRPC](https://grpc.io/), [Protocol Buffers](https://developers.google.com/protocol-buffers)
and [VirusTotal API](https://developers.virustotal.com/v3.0/reference). It is included in the Django App.

## Trash Cleaning Microservice

The application provides an automated cleaning service for the files that are uploaded to the server. 
The files are deleted after a certain period of time (ttl).
The time period can be set in the `.env` file. (`TRASH_TIMEOUT`)

This service will periodically check redis for the files that have expired and delete them from the server's storage.