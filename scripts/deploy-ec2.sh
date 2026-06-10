#!/bin/bash
# Run on EC2 after git pull (or via GitHub Actions SSH).
# Rebuilds changed images and restarts containers. Data volumes are preserved.

set -euo pipefail

REPO_DIR="${DEPLOY_PATH:-$HOME/Multi-Tenant-Enterprise-Knowledge-Platform-RAG-}"

echo "==> Deploy target: $REPO_DIR"

if [ ! -d "$REPO_DIR/.git" ]; then
  echo "ERROR: Repo not found at $REPO_DIR"
  echo "Clone on EC2: git clone https://github.com/Uday-Polineni/Multi-Tenant-Enterprise-Knowledge-Platform-RAG-.git"
  exit 1
fi

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
for i in $(seq 1 36); do
  if curl -sf http://localhost/health >/dev/null; then
    echo "OK  GET /health"
    docker compose ps
    exit 0
  fi
  sleep 5
done

echo "ERROR: /health did not return OK within 180s"
docker compose ps
docker compose logs api --tail 40
docker compose logs web --tail 20
exit 1
