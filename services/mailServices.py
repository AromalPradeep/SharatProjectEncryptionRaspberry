import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
import datetime
from dotenv import load_dotenv

load_dotenv()
    
def send_email(subject, message, receiver_email):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sender_email = "sxrxths@zohomail.in"
    smtp_server = "smtp.zoho.in"
    smtp_port = 465  # For SSL
    smtp_username = os.getenv("smtp_username")
    smtp_password = os.getenv("smtp_password")

    # Make each email subject and message distinct
    subject = f"{subject} - {timestamp}"
    message = f"{message}\n\nSent at {timestamp}"

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(message, 'plain'))

    # Create SMTP session
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        # Login to SMTP server
        server.login(smtp_username, smtp_password)
        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        
