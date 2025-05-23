#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
ROOTDIR=$(pwd)

VERSION=$(git rev-parse --short HEAD)

PROJECT="astro-bot-424018" 
ENVIRONMENT="prod"
CLOUD_RUN_MIN_INSTANCE_COUNT=0
CLOUD_RUN_MAX_INSTANCE_COUNT=3
REGION="europe-west4"
IMAGE=europe-west1-docker.pkg.dev/astro-bot-424018/astro-bot/images:latest

echo "Deploying to ${PROJECT} (${ENVIRONMENT}) with version ${VERSION}..."

poetry run mypy main.py

gcloud builds submit --config cloudbuild.cloud-run.yaml \
        --project $PROJECT \
        --region "europe-west1"
gcloud run deploy backend --image=$IMAGE \
      --env-vars-file="${ENVIRONMENT}.cloudrun.env.yaml" --project ${PROJECT} --region $REGION \
      --allow-unauthenticated \
      --cpu=1 --memory=3Gi --concurrency=200 \
      --max-instances=$CLOUD_RUN_MAX_INSTANCE_COUNT \
      --min-instances=$CLOUD_RUN_MIN_INSTANCE_COUNT \
      --no-cpu-throttling
