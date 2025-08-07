# Google Cloud Platform Deployment Guide

Deploy your Mobile Food Vendor Permit app to Google Cloud Run - a serverless platform that's perfect for containerized applications.

## 🎯 Why Google Cloud Run?

- **Serverless**: No server management required
- **Auto-scaling**: Scales from 0 to thousands of instances
- **Pay-per-use**: Only pay when your app is serving requests
- **Container-native**: Direct Docker support
- **Global**: Deploy to multiple regions easily

## 📋 Prerequisites

### 1. Install Google Cloud SDK
```bash
# macOS
brew install --cask google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### 2. Create GCP Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable billing for the project

### 3. Authenticate
```bash
gcloud auth login
gcloud auth configure-docker
```

## 🚀 Quick Deployment

### Method 1: Using the Deploy Script (Recommended)

1. **Update the script with your project ID:**
   ```bash
   # Edit deploy-gcp.sh
   PROJECT_ID="your-actual-gcp-project-id"
   ```

2. **Make script executable and run:**
   ```bash
   chmod +x deploy-gcp.sh
   ./deploy-gcp.sh
   ```

### Method 2: Manual Deployment

1. **Set up gcloud:**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud config set run/region us-central1
   ```

2. **Enable APIs:**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   ```

3. **Deploy Backend:**
   ```bash
   gcloud run deploy vendor-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000
   ```

4. **Deploy Frontend:**
   ```bash
   cd frontend/vendor-search
   gcloud run deploy vendor-frontend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 80
   ```

## 🔧 Configuration Options

### Backend Service Settings
```bash
--memory 1Gi                 # Memory allocation
--cpu 1                      # CPU allocation
--max-instances 10           # Maximum instances
--min-instances 0            # Minimum instances (scales to zero)
--timeout 300                # Request timeout (seconds)
```

### Frontend Service Settings
```bash
--memory 512Mi               # Smaller memory for static files
--cpu 1                      # CPU allocation
--max-instances 5            # Lower max instances
```

### Environment Variables
```bash
--set-env-vars KEY=VALUE     # Set environment variables
--env-vars-file .env         # Load from file
```

## 🌐 Custom Domains

### Add Custom Domain
1. Go to Cloud Run service in console
2. Click "Manage Custom Domains"
3. Add your domain
4. Update DNS records as instructed

### SSL Certificates
- Automatic HTTPS certificates are provided
- Custom certificates can be uploaded if needed

## 📊 Monitoring and Logging

### View Logs
```bash
# Backend logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=vendor-backend"

# Frontend logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=vendor-frontend"
```

### Monitoring Dashboard
- Go to Google Cloud Console
- Navigate to Cloud Run
- Click on your service
- View metrics, logs, and revisions

## 💰 Cost Optimization

### Free Tier Limits
- 2 million requests per month
- 400,000 GB-seconds of memory
- 200,000 vCPU-seconds of compute time

### Cost Optimization Tips
1. **Use minimum instances = 0** (scales to zero)
2. **Right-size memory and CPU** (start small, scale up)
3. **Set appropriate timeouts**
4. **Use Cloud Build for CI/CD** (automate deployments)

## 🔒 Security Best Practices

### IAM and Authentication
```bash
# Create service account for app
gcloud iam service-accounts create vendor-app-sa

# Grant minimal permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:vendor-app-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

### Environment Variables
- Store secrets in Google Secret Manager
- Use IAM for access control
- Never commit secrets to code

## 🔄 CI/CD with Cloud Build

### Enable Continuous Deployment
1. Connect your GitHub repository to Cloud Build
2. Use the provided `cloudbuild.yaml`
3. Trigger builds on commits to main branch

### Manual Trigger
```bash
gcloud builds submit --config cloudbuild.yaml .
```

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**
   ```bash
   # Check build logs
   gcloud builds list
   gcloud builds log BUILD_ID
   ```

2. **Service Won't Start**
   ```bash
   # Check service logs
   gcloud logs read "resource.type=cloud_run_revision"
   ```

3. **Port Issues**
   - Ensure Dockerfile exposes correct port
   - Match port in gcloud deploy command

4. **Memory/CPU Issues**
   - Increase memory allocation
   - Check application resource usage

### Debug Commands
```bash
# Service details
gcloud run services describe SERVICE_NAME --region=REGION

# Revision details
gcloud run revisions describe REVISION_NAME --region=REGION

# Service status
gcloud run services list
```

## 📈 Scaling Configuration

### Auto-scaling Settings
```bash
--min-instances 1            # Always warm (costs more)
--max-instances 100          # Maximum concurrent instances
--concurrency 80             # Requests per instance
```

### Traffic Splitting
```bash
# Deploy new revision with no traffic
gcloud run deploy --no-traffic

# Gradually shift traffic
gcloud run services update-traffic SERVICE_NAME \
  --to-revisions=NEW_REVISION=50,OLD_REVISION=50
```

## 🎉 Post-Deployment

### Test Your Application
1. **Frontend**: Visit the provided Cloud Run URL
2. **Backend API**: Visit `{backend-url}/docs` for Swagger UI
3. **Health Check**: Test all three search types

### Share Your App
- Frontend URL: For users to interact with your app
- API URL: For developers to integrate with your API
- Documentation: Share the `/docs` endpoint for API docs

## 💡 Next Steps

1. **Set up monitoring alerts**
2. **Add custom domain**
3. **Implement authentication if needed**
4. **Set up automated backups**
5. **Add more regions for global deployment**

---

**🔗 Useful Links:**
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Best Practices](https://cloud.google.com/run/docs/best-practices)
