## Run on Local Environment

```
docker build -t segment-api .
docker run -p 8080:8080 segment-api
```

## Deploy Build on Gcloud

Example script for deploying build on GCP

```
gcloud run deploy segment-api \
  --image gcr.io/your_gcp_project_id/segment-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars BASE_DOMAIN=your_base_domain,SEGMENT_WRITE_KEY=your_segment_api_key,API_KEYS=your_custom_api_key
```