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

```bash
# Run backend & frontend using docker-compose
docker-compose up

#Run frontend using docker-compose
docker compose -f  docker-compose-frontend.yml up -d

# Run backend using kubernetes
cd K8s
kubectl apply -f redis_deployment.yaml
kubectl apply -f backend_deployment.yaml
kubectl apply -f backend_service.yaml

# Run frontend locally
cd ../safeshare-frontend
npm install
npm start
```

## Endpoints

- `/admin/` - Admin Panel
- `/api/` - API Root
