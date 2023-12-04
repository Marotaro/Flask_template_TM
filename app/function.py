from datetime import date
import smtplib
from app.config import MDP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def datenow():
    today= date.today()
    return today.strftime("%d/%m/%Y")




def send_email(to_email, message, subject):
    HOST = "smtp.office365.com"
    PORT = 587
    FROM_EMAIL = r"y.sender@outlook.com"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Cc'] = FROM_EMAIL
    msg['Bcc'] = FROM_EMAIL
    msg.attach(MIMEText(message, 'html'))
    try:
        with smtplib.SMTP(HOST, port = PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(FROM_EMAIL, MDP)

            # Send the email
            smtp.send_message(msg)
            print('Email sent successfully.')
    except Exception as e:
        print(f'Error: {e}')
