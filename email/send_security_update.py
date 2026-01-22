#!/usr/bin/env python3
import argparse
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).resolve().parent / "security_update_email.html"


def build_message(sender: str, recipient: str, subject: str, html_body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(
        "Votre client mail ne prend pas en charge le HTML. Merci d'ouvrir ce message dans un client compatible."
    )
    message.add_alternative(html_body, subtype="html")
    return message


def send_email(
    message: EmailMessage,
    host: str,
    port: int,
    username: str | None,
    password: str | None,
    use_tls: bool,
    use_ssl: bool,
) -> None:
    smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_class(host=host, port=port, timeout=10) as smtp:
        smtp.ehlo()
        if use_tls and not use_ssl:
def send_email(message: EmailMessage, host: str, port: int, username: str | None, password: str | None, use_tls: bool) -> None:
    with smtplib.SMTP(host=host, port=port, timeout=10) as smtp:
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
            smtp.ehlo()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)


def main() -> None:
    parser = argparse.ArgumentParser(description="Envoyer l'email HTML de mise à jour de sécurité via Poste.io.")
    parser.add_argument("--to", dest="recipient", default=os.getenv("SMTP_TO"))
    parser.add_argument("--from", dest="sender", default=os.getenv("SMTP_FROM"))
    parser.add_argument("--subject", default=os.getenv("SMTP_SUBJECT", "Mise à jour de sécurité — action urgente requise"))
    parser.add_argument("--template", default=os.getenv("SMTP_TEMPLATE", str(DEFAULT_TEMPLATE)))
    parser.add_argument("--host", default=os.getenv("SMTP_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SMTP_PORT", "25")))
    parser.add_argument("--username", default=os.getenv("SMTP_USER"))
    parser.add_argument("--password", default=os.getenv("SMTP_PASSWORD"))
    parser.add_argument("--no-tls", action="store_true", help="Désactiver STARTTLS")
    parser.add_argument("--use-ssl", action="store_true", default=os.getenv("SMTP_USE_SSL", "false").lower() == "true")
    parser.add_argument("--host", default=os.getenv("SMTP_HOST", "mail.example.com"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SMTP_PORT", "587")))
    parser.add_argument("--username", default=os.getenv("SMTP_USER"))
    parser.add_argument("--password", default=os.getenv("SMTP_PASSWORD"))
    parser.add_argument("--no-tls", action="store_true", help="Désactiver STARTTLS")

    args = parser.parse_args()

    if not args.recipient or not args.sender:
        raise SystemExit("Les champs --to et --from (ou SMTP_TO/SMTP_FROM) sont obligatoires.")

    template_path = Path(args.template).expanduser()
    html_body = template_path.read_text(encoding="utf-8")

    message = build_message(args.sender, args.recipient, args.subject, html_body)
    send_email(
        message,
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        use_tls=not args.no_tls,
        use_ssl=args.use_ssl,
    )
    print(f"Email envoyé à {args.recipient} via {args.host}:{args.port}.")


if __name__ == "__main__":
    main()
