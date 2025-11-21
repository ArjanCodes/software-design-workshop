from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol

# -------------------------
# SMTP Interface (via Protocol)
# -------------------------


class SMTPInterface(Protocol):
    def connect(self, host: str, port: int): ...
    def starttls(self): ...
    def login(self, login: str, password: str): ...
    def sendmail(self, from_addr: str, to_addr: str, message: str): ...
    def quit(self): ...


# -------------------------
# FakeSMTP (test/mock implementatie)
# -------------------------


class FakeSMTP:
    def connect(self, host: str, port: int):
        print(f"[FakeSMTP] Connecting to {host}:{port}")

    def starttls(self):
        print("[FakeSMTP] Starting TLS")

    def login(self, login: str, password: str):
        print(f"[FakeSMTP] Logging in as {login}")

    def sendmail(self, from_addr: str, to_addr: str, message: str):
        print(f"[FakeSMTP] Sending email from {from_addr} to {to_addr}")
        print("---- BEGIN MESSAGE ----")
        print(message)
        print("---- END MESSAGE ----")

    def quit(self):
        print("[FakeSMTP] Closing connection")


# -------------------------
# E-mail builder
# -------------------------


def build_message(
    from_address: str, to_address: str, subject: str, content: str
) -> str:
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    mime = MIMEText(
        content,
        "html" if content.lower().startswith("<!doctype html>") else "plain",
    )
    msg.attach(mime)
    return msg.as_string()


# -------------------------
# Main email-sending function (met injectie)
# -------------------------


def send_email(
    smtp: SMTPInterface,
    smtp_host: str,
    smtp_port: int,
    login: str,
    password: str,
    from_address: str,
    to_address: str,
    subject: str,
    message: str,
):
    smtp.connect(smtp_host, smtp_port)
    smtp.starttls()
    smtp.login(login, password)

    mime_message = build_message(from_address, to_address, subject, message)
    smtp.sendmail(from_address, to_address, mime_message)

    smtp.quit()


# -------------------------
# Main functie (voorbeeld)
# -------------------------


def main():
    smtp = FakeSMTP()

    send_email(
        smtp=smtp,
        smtp_host="smtp.example.com",
        smtp_port=587,
        login="admin",
        password="super_secret_password",
        from_address="me@example.com",
        to_address="you@example.com",
        subject="Refactored Email",
        message="This email was sent using dependency injection 🚀",
    )


if __name__ == "__main__":
    main()
