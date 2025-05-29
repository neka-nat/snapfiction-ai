# Snapfiction AI

This is an AI agent that generates a short story movie from a prompt.

## Demo
https://github.com/user-attachments/assets/b31ccf3b-58d8-4dcb-8db4-9e186759ac50

https://github.com/user-attachments/assets/22b7388e-aac7-4cf9-beb1-3c6a52159ef4

https://github.com/user-attachments/assets/f0b2a3cc-faa4-40ae-9875-06f3c116f83d

https://github.com/user-attachments/assets/f1a1f795-cf09-4ffb-927e-678d6c428e5b


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

