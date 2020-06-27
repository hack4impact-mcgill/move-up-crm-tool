import os
from flask import Flask, render_template
from flask_mail import Mail, Message

from app import create_app, mail


def send_email(recipients, subject, message, **kwargs):
    app = create_app(os.getenv("FLASK_CONFIG") or "default")
    with app.app_context():
        msg = Message(
            app.config["EMAIL_SUBJECT_PREFIX"] + " " + subject,
            sender=app.config["EMAIL_SENDER"],
            recipients=recipients,
            body=message,
        )

        mail.send(msg)
