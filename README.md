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