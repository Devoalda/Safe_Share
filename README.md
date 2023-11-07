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

### Prerequisites

Before you begin, make sure you have:

- A Kubernetes cluster up and running.
- `kubectl` installed and configured to communicate with your cluster.
- Proper permissions to create Deployments, Services, Persistent Volumes, and other Kubernetes resources.

### Overview of Components

- `frontend_deployment.yaml`: Deployment for the SafeShare frontend.
- `frontend_service.yaml`: Service exposing the SafeShare frontend.
- `backend_deployment.yaml`: Deployment for the SafeShare backend.
- `backend_service.yaml`: Service exposing the SafeShare backend.
- `redis_deployment.yaml`: Setup for Redis with persistent storage.

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

## Test Files

Theoretically, the application can handle any type of file. However, we have tested the application with the following file types:
- Text-based `.txt`, `.py`, etc.
- Image-based `.png`, `.jpg`, etc.
- Video-based `.mp4`, etc.
- Executable `.exe`, etc.

The Virus file used for testing is generated with [metasploit](https://www.metasploit.com/) (msfvenom). ([VirusTotal Report](https://www.virustotal.com/gui/file/2fd0c13298f99d5ae10765ef65e1667e205e932376396d92e4343468abe0c541/detection))

It is a simple reverse shell payload that connects to the attacker's machine, Harmless since it is not connected to the attacker's machine. But **DO NOT** run it on your machine.
