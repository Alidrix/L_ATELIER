#!/usr/bin/env python3
import argparse
import imaplib
import os
import shutil
import subprocess
import time


def notify(summary: str, body: str) -> None:
    notifier = shutil.which("notify-send")
    if notifier:
        subprocess.run([notifier, summary, body], check=False)
    else:
        print(f"[notification] {summary}: {body}")


def check_unseen(imap: imaplib.IMAP4, mailbox: str) -> int:
    imap.select(mailbox)
    status, data = imap.search(None, "UNSEEN")
    if status != "OK":
        return 0
    ids = data[0].split()
    return len(ids)


def main() -> None:
    parser = argparse.ArgumentParser(description="Notifier l'arrivée de nouveaux emails (Poste.io IMAP).")
    parser.add_argument("--host", default=os.getenv("IMAP_HOST", "mail.local"))
    parser.add_argument("--port", type=int, default=int(os.getenv("IMAP_PORT", "143")))
    parser.add_argument("--username", default=os.getenv("IMAP_USER"))
    parser.add_argument("--password", default=os.getenv("IMAP_PASSWORD"))
    parser.add_argument("--mailbox", default=os.getenv("IMAP_MAILBOX", "INBOX"))
    parser.add_argument("--interval", type=int, default=int(os.getenv("IMAP_POLL_INTERVAL", "20")))
    parser.add_argument("--use-ssl", action="store_true", default=os.getenv("IMAP_USE_SSL", "false").lower() == "true")
    args = parser.parse_args()

    if not args.username or not args.password:
        raise SystemExit("IMAP_USER et IMAP_PASSWORD sont requis.")

    last_unseen = 0
    while True:
        try:
            if args.use_ssl:
                imap = imaplib.IMAP4_SSL(args.host, args.port)
            else:
                imap = imaplib.IMAP4(args.host, args.port)
            imap.login(args.username, args.password)
            unseen = check_unseen(imap, args.mailbox)
            imap.logout()

            if unseen > last_unseen:
                notify("Nouveau mail reçu", f"{unseen} message(s) non lu(s) dans {args.mailbox}.")
            last_unseen = unseen
        except Exception as exc:
            notify("Surveillance mail", f"Erreur IMAP : {exc}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
