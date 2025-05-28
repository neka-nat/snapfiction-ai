# Snapfiction AI

This is an AI agent that generates a short story movie from a prompt.

## Requirements

- Python 3.12
- Google ADK
- Gemini on Vertex AI
- Google Cloud Storage
- Imagen (Image Generation)
- Lyria (Music Generation)
- Veo (Video Generation)

## Setup

```bash
uv sync
```

### Google Cloud

This application uses Google Cloud Storage to store videos.

First, you need to create a bucket.
Second, you need to add the service account(cloud-lvm-video-server@prod.google.com) to the bucket.

This service account is used for video generation by Vertex AI.

```bash
gcloud auth login
gcloud storage buckets create \
  gs://<your-bucket-name> \
  --default-storage-class=standard \
  --location=<your-region> \
  --uniform-bucket-level-access
gcloud storage buckets add-iam-policy-binding \
  gs://<your-bucket-name> \
  --member=serviceAccount:cloud-lvm-video-server@prod.google.com \
  --role=roles/storage.objectUser
```


## Run

```bash
uv run adk web
```

