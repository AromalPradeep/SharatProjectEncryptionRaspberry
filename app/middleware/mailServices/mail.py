import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, receiver_email):
    
    sender_email = "your_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 465  # For SSL
    smtp_username = "your_smtp_username"
    smtp_password = "your_smtp_password"


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
        
