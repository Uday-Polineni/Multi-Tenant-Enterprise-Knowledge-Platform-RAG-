#!/bin/sh
set -e

export NGINX_HOST="${NGINX_HOST:-_}"

CERT="/etc/letsencrypt/live/${NGINX_HOST}/fullchain.pem"

if [ -f "$CERT" ]; then
  echo "TLS cert found — enabling HTTPS for ${NGINX_HOST}"
  envsubst '${NGINX_HOST}' < /etc/nginx/templates/nginx.ssl.conf.template > /etc/nginx/conf.d/default.conf
else
  echo "No TLS cert yet — HTTP only (run setup-https.sh on EC2)"
  envsubst '${NGINX_HOST}' < /etc/nginx/templates/nginx.init.conf.template > /etc/nginx/conf.d/default.conf
fi

exec nginx -g 'daemon off;'
