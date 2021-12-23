import email, smtplib, ssl
import os
import configparser

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read("config")

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
ADDRESS = config["email"]["EMAIL_ADDRESS"]
PASSWORD = config["email"]["EMAIL_PASSWORD"]

def create_message(to_addr, subject, html):
    message = MIMEMultipart()
    message["From"] = ADDRESS
    message["To"] = to_addr
    message["Subject"] = subject
    
    message.attach(MIMEText(html, "html"))
    return message

def send_msg(message):
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls(context=context)
        server.login(ADDRESS, PASSWORD)
        server.sendmail(ADDRESS, "mh7289@student.uni-lj.si", message.as_string())
    finally:
        server.quit()
    