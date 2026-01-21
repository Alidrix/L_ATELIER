#!/bin/sh
set -eu

TARGET_DIR="$HOME/.local/share/securityupdate"
SYSTEMD_DIR="$HOME/.config/systemd/user"

mkdir -p "$TARGET_DIR" "$SYSTEMD_DIR"

cp "$(dirname "$0")/notify_new_mail.py" "$TARGET_DIR/notify_new_mail.py"
cp "$(dirname "$0")/notify-mail.service" "$SYSTEMD_DIR/notify-mail.service"
cp "$(dirname "$0")/notify-mail.timer" "$SYSTEMD_DIR/notify-mail.timer"

systemctl --user daemon-reload
systemctl --user enable --now notify-mail.timer

echo "Notification installée. Pensez à définir IMAP_USER/IMAP_PASSWORD dans votre environnement utilisateur." 
