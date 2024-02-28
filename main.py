import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import pandas as pd
from jinja2 import Environment, FileSystemLoader

template_path = "your.html.jinja"
template_format = "html"
recipients_path = "your.recipients.csv"
subject = "Your subject goes here"

# Load recipients data
data = pd.read_csv(recipients_path, dtype=str)

# Load email template
env = Environment(loader=FileSystemLoader(searchpath=""))
template = env.get_template(template_path)

# Load env variables
load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
SENDER_NAME = os.getenv('SENDER_NAME')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

sender = SENDER_ADDRESS
sender_name = SENDER_NAME
ccs = []
password = SENDER_PASSWORD

def send_email(subject, body, sender, sender_name, recipients, ccs, password, format="html"):
    msg = MIMEText(body, format)
    msg['Subject'] = subject
    msg['From'] = sender_name
    msg['To'] = ', '.join(recipients)
    msg['Cc'] = ', '.join(ccs)
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients + ccs, msg.as_string())
    print(f"Message sent to {recipients}!")

for index, row in data.iterrows():
    email = row["email"]
    body = template.render(**row.to_dict())

    print(body)

    send_email(
        subject=subject, 
        body=body, 
        sender=sender, 
        sender_name=sender_name, 
        recipients=[email], 
        ccs=ccs, 
        password=password, 
        format=template_format
    )