#!/bin/bash

# Google Cloud Run Deployment Script for Mobile Food Vendor Permit App
# Make sure you have gcloud CLI installed and authenticated

set -e

# Configuration
PROJECT_ID="your-gcp-project-id"  # Replace with your GCP project ID
REGION="us-central1"
BACKEND_SERVICE="vendor-backend"
FRONTEND_SERVICE="vendor-frontend"

echo "🚀 Deploying Mobile Food Vendor Permit App to Google Cloud Run"

# Set up gcloud configuration
echo "📝 Setting up gcloud configuration..."
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Deploy Backend (FastAPI)
echo "🐍 Deploying FastAPI Backend..."
gcloud run deploy $BACKEND_SERVICE \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars ENVIRONMENT=production

# Get backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format='value(status.url)')
echo "✅ Backend deployed at: $BACKEND_URL"

# Deploy Frontend (React)
echo "⚛️  Deploying React Frontend..."
cd frontend/vendor-search

# Update environment for production
echo "REACT_APP_API_URL=$BACKEND_URL" > .env.production

gcloud run deploy $FRONTEND_SERVICE \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 80 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 5

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format='value(status.url)')

echo "🎉 Deployment Complete!"
echo "📱 Frontend: $FRONTEND_URL"
echo "🔗 Backend: $BACKEND_URL"
echo "📚 API Docs: $BACKEND_URL/docs"

cd ../..

echo "💡 Next steps:"
echo "1. Test your app at $FRONTEND_URL"
echo "2. Check API documentation at $BACKEND_URL/docs"
echo "3. Monitor your services in the GCP Console"
