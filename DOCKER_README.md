# Docker Setup for Mobile Food Vendor Permit App

This guide covers how to run the complete application (FastAPI backend + React frontend) using Docker.

## 🐳 Prerequisites

- Docker installed on your system
- Docker Compose installed (usually comes with Docker Desktop)

## 📁 Project Structure

```
MobileFoodVendorPermit/
├── Dockerfile                     # FastAPI backend
├── docker-compose.yml            # Orchestrates both services
├── .dockerignore                 # Backend build optimizations
├── app/                          # FastAPI application
├── tests/                        # Backend tests (included in Docker)
├── requirements.txt              # Python dependencies
├── main.py                       # FastAPI entry point
├── Mobile_Food_Facility_Permit_cleansed.csv
└── frontend/vendor-search/
    ├── Dockerfile                # React frontend
    ├── .dockerignore            # Frontend build optimizations
    ├── nginx.conf               # Production web server config
    └── src/                     # React application
```

## 🚀 Quick Start

### Run Everything with Docker Compose

```bash
# From the project root directory
docker-compose up --build
```

This will:
- Build both backend and frontend images
- Start FastAPI backend on http://localhost:8000
- Start React frontend on http://localhost:3000
- Set up networking between services

### Individual Service Commands

#### Backend Only
```bash
# Build backend image
docker build -t vendor-backend .

# Run backend container
docker run -p 8000:8000 vendor-backend
```

#### Frontend Only
```bash
# Build frontend image
cd frontend/vendor-search
docker build -t vendor-frontend .

# Run frontend container
docker run -p 3000:80 vendor-frontend
```

## 🔧 Development vs Production

### Development Mode
The docker-compose.yml includes volume mounts for development:
```yaml
volumes:
  - ./app:/app/app        # Live reload for backend changes
  - ./tests:/app/tests    # Access to tests
```

### Production Mode
For production, remove the volume mounts and use:
```bash
docker-compose up --build -d
```

## 🧪 Running Tests in Docker

### Backend Tests
```bash
# Run tests in the backend container
docker-compose exec backend pytest

# Or run tests during build (add to Dockerfile if needed)
docker-compose exec backend python -m pytest tests/
```

### Build-time Testing
You can modify the backend Dockerfile to run tests during build:
```dockerfile
# Add before the CMD instruction
RUN python -m pytest tests/ --verbose
```

## 🌐 Environment Configuration

### Backend Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
DEBUG=False
```

### Frontend Environment Variables
The frontend uses `REACT_APP_API_URL` to connect to the backend:
- Development: `http://localhost:8000`
- Production: Update in docker-compose.yml or .env files

## 📊 Health Checks

The backend service includes a health check:
```bash
# Check backend health
curl http://localhost:8000/docs

# View health status
docker-compose ps
```

## 🔍 Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml if 3000 or 8000 are in use
2. **CORS errors**: Ensure REACT_APP_API_URL matches your backend URL
3. **Build failures**: Check .dockerignore files aren't excluding needed files

### Useful Commands

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Stop all services
docker-compose down

# Remove all containers and volumes
docker-compose down -v

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 🚢 Production Deployment

### Using Docker Hub
```bash
# Tag and push images
docker tag vendor-backend your-registry/vendor-backend:latest
docker tag vendor-frontend your-registry/vendor-frontend:latest

docker push your-registry/vendor-backend:latest
docker push your-registry/vendor-frontend:latest
```

### Using Docker Swarm
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml vendor-app
```

### Environment-specific Configs
Create separate compose files:
- `docker-compose.yml` (base)
- `docker-compose.prod.yml` (production overrides)
- `docker-compose.dev.yml` (development overrides)

```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📈 Monitoring

### Container Stats
```bash
docker stats
docker-compose top
```

### Resource Usage
```bash
# Memory and CPU usage
docker system df
docker system prune  # Clean up unused resources
```

## 🔒 Security Notes

- The nginx configuration includes security headers
- Use secrets management for production credentials
- Consider using non-root users in containers
- Regularly update base images for security patches

## 🎯 Next Steps

- Set up CI/CD pipeline with Docker builds
- Add database service to docker-compose
- Implement log aggregation
- Set up monitoring with Prometheus/Grafana
- Configure reverse proxy (nginx/traefik) for production
