#!/bin/sh
set -eu

HOSTS_ENTRY="127.0.0.1 portal.example.com"
MAIL_ENTRY="127.0.0.1 mail.local"

if ! grep -q "portal.example.com" /etc/hosts; then
  echo "Adding portal.example.com to /etc/hosts"
  printf "%s\n" "$HOSTS_ENTRY" | sudo tee -a /etc/hosts >/dev/null
fi

if ! grep -q "mail.local" /etc/hosts; then
  echo "Adding mail.local to /etc/hosts"
  printf "%s\n" "$MAIL_ENTRY" | sudo tee -a /etc/hosts >/dev/null
fi
