#!/bin/sh

set -e

echo "Starting RAG ingestion..."

python ingest.py

echo "RAG ingestion completed."

echo "Starting FastAPI..."

exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"