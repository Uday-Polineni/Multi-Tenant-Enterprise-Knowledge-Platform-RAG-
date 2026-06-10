#!/bin/bash
# Run on EC2 after git pull (or via GitHub Actions SSH).
# Rebuilds changed images and restarts containers. Data volumes are preserved.

set -euo pipefail

REPO_DIR="${DEPLOY_PATH:-$HOME/Multi-Tenant-Enterprise-Knowledge-Platform-RAG-}"

cd "$REPO_DIR"
git fetch origin main
git reset --hard origin/main

cd docker

if [ ! -f .env ]; then
  echo "ERROR: docker/.env missing — create from .env.example on the server first."
  exit 1
fi

docker compose up --build -d

echo "Waiting for health check..."
for i in $(seq 1 30); do
  if curl -sf http://localhost/health >/dev/null; then
    echo "OK  GET /health"
    docker compose ps
    exit 0
  fi
  sleep 5
done

echo "ERROR: /health did not return OK within 150s"
docker compose logs api --tail 40
exit 1
