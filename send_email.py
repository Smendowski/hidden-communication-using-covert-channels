from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl
import lorem
import os

sender_email = os.environ.get("SCS_SENDER_EMAIL")
receiver_email = os.environ.get("SCS_RECEIVER_EMAIL")
password = os.environ.get("SCS_EMAIL_PASSWORD")

if None in [password, sender_email, receiver_email]:
  print("Set the necessary environment variables.")
  raise SystemExit


message = MIMEMultipart("alternative")
message["Subject"] = "SCS2021"
message["From"] = sender_email
message["To"] = receiver_email

hidden_information = ("".join([lorem.text() for _ in range(5)])).replace("\n", "")

message.add_header('SCS2021', "%s" % hidden_information)

content = """\
Hi,
Are You able to find me?
"""

mail_content = MIMEText(content, "plain")
message.attach(mail_content)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
