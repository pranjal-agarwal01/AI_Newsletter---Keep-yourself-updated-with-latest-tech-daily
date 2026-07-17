"""Email delivery adapter. Phase 1: Gmail SMTP with an app password.
Keep the send() signature stable — SendGrid/Telegram adapters replace this later."""
from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from .config import env

log = logging.getLogger(__name__)


def send(subject: str, html_body: str, text_body: str) -> None:
    sender = env("GMAIL_ADDRESS")
    password = env("GMAIL_APP_PASSWORD")
    recipient = env("DIGEST_TO", sender)

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    log.info("deliver: sent '%s' to %s", subject, recipient)
