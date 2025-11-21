from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


class EmailClient:
    def __init__(self):
        # Hardcoded SMTP server + credentials
        self._server = SMTP()
        self._server._host = "smtp.example.com:587"  # type: ignore
        self._host, _port = "smtp.example.com:587".split(":")
        self._port = int(_port)
        self._login = "admin"
        self._password = "super_secret_password"
        self.to_address = "support@example.com"

    def _connect(self) -> None:
        # Hardcoded TLS behaviour
        self._server.connect(self._host, self._port)
        self._server.starttls()
        self._server.login(self._login, self._password)

    def _quit(self) -> None:
        self._server.quit()

    def send_message(
        self,
        from_address: str,
        to_address: str | None = None,
        subject: str = "No subject",
        message: str = "",
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address or self.to_address
        msg["Subject"] = subject

        mime = MIMEText(
            message,
            "html" if message.lower().startswith("<!doctype html>") else "plain",
        )
        msg.attach(mime)

        # Tight coupling: direct connect + sendmail + quit
        self._connect()
        self._server.sendmail(msg["From"], msg["To"], msg.as_string())
        self._quit()


def main():
    client = EmailClient()
    client.send_message(
        from_address="me@example.com",
        subject="Hello!",
        message="This is a tightly coupled email client.",
    )


if __name__ == "__main__":
    main()
