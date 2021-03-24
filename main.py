import smtplib
import ssl
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465

account = input("Mail address: ")
password = input("Password: ")

subject = input("Enter subject of your e-mails: ")

receiver = ""

message = MIMEMultipart("alternative")
message["Subject"] = subject
message["From"] = '<' + account + '>'

f_text = open("plaintext.txt", "r", encoding="utf-8")
text = f_text.read()
part1 = MIMEText(text, "plain", 'UTF-8')

if text != "null":
    message.attach(part1)
else:
    print("Notification: Plaintext file did not attached to mail message because of it has specified with null.")

f_html = open("html.html", "r", encoding="utf-8")
html = f_html.read()
part2 = MIMEText(html, "html", 'UTF-8')

if html != "null":
    message.attach(part2)
else:
    print("Notification: Html file did not attached to mail message because of it has specified with null.")

attachmentFileName = input("Enter attachment name: ")

with open(attachmentFileName, "rb") as attachment:
    part3 = MIMEBase("application", "octet-stream")
    part3.set_payload(attachment.read())

encoders.encode_base64(part3)
part3.add_header("Content-Disposition", f"attachment; filename= {attachmentFileName}")

if attachmentFileName == "null":
    print("Notification: Attachment file did not attached to mail message because of it has specified with null.")
else:
    message.attach(part3)

print("Send e-mails? (type yes or no): ")
isUserSure = input()
if isUserSure == "no":
    exit(0)
elif isUserSure == "yes":
    print("Sending e-mails...")
else:
    print("invalid input exiting from program")
    exit(1)

f_receivers = open("receivers.txt", "r")

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(account, password)
    while f_receivers.readable():
        receiver = ""
        receiver = f_receivers.readline()
        message["To"] = '<' + receiver + '>'
        server.sendmail(account, receiver, message.as_string())
        print("Mail has sent to " + receiver)
    server.quit()

print("Sending completed successfully.")
time.sleep(3)

f_html.close()
f_text.close()
f_receivers.close()
