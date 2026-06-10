#!/bin/bash
# Free HTTPS with Let's Encrypt on the EC2 public DNS hostname.
# Run on EC2 from the docker/ directory after the app is up on HTTP.
#
# Usage:
#   chmod +x setup-https.sh
#   ./setup-https.sh your@email.com
#
# Requires NGINX_HOST in .env (EC2 Public IPv4 DNS).

set -euo pipefail

EMAIL="${1:-}"
if [ -z "$EMAIL" ]; then
  echo "Usage: ./setup-https.sh your@email.com"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f .env ]; then
  echo "Missing .env — copy from .env.example first."
  exit 1
fi

# shellcheck disable=SC1091
source .env

if [ -z "${NGINX_HOST:-}" ]; then
  echo "Set NGINX_HOST in .env to your EC2 Public IPv4 DNS, e.g.:"
  echo "NGINX_HOST=ec2-3-15-42-88.us-east-2.compute.amazonaws.com"
  exit 1
fi

WEBROOT="${CERTBOT_WEBROOT:-/var/www/certbot}"

sudo mkdir -p "$WEBROOT"

echo "==> Restarting web (HTTP + ACME challenge path)..."
docker compose up -d web

echo "==> Requesting certificate for ${NGINX_HOST}..."
if ! command -v certbot >/dev/null 2>&1; then
  sudo apt-get update
  sudo apt-get install -y certbot
fi

sudo certbot certonly --webroot \
  -w "$WEBROOT" \
  -d "$NGINX_HOST" \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  --non-interactive

echo "==> Restarting web with HTTPS..."
docker compose restart web

echo ""
echo "Done. Open: https://${NGINX_HOST}"
echo "Renewal (add to crontab):"
echo "  0 3 * * * certbot renew --webroot -w $WEBROOT --quiet && cd $SCRIPT_DIR && docker compose restart web"
