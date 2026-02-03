#!/bin/sh
set -eu

CERT_DIR="/etc/nginx/ssl"
CERT_FILE="${CERT_DIR}/portal.example.crt"
KEY_FILE="${CERT_DIR}/portal.example.key"

if [ ! -s "$CERT_FILE" ] || [ ! -s "$KEY_FILE" ]; then
  echo "[nginx] Generating self-signed TLS certificate for portal.example.com"
  mkdir -p "$CERT_DIR"
  openssl req -x509 -nodes -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -days 365 \
    -subj "/CN=portal.example.com" \
    -addext "subjectAltName=DNS:portal.example.com"
fi
