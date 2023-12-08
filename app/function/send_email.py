#smtplib est une librairie rajoutée, il faut donc la téléchargée 
import smtplib
from app.config import MDP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, message, subject):
    #Information de connection
    HOST = "smtp.office365.com"
    PORT = 587
    FROM_EMAIL = r"y.sender@outlook.com"

    #Information général de l'envoie
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Cc'] = FROM_EMAIL
    msg['Bcc'] = FROM_EMAIL

    #Message peut être une simple chaine de caractères pour ceci il suffit de remplacer MIMEText(message,'plain')
    msg.attach(MIMEText(message, 'html'))
    try:
        with smtplib.SMTP(HOST, port = PORT) as smtp:
            #Connection au serveur smtp
            smtp.ehlo()
            smtp.starttls()
            #MDP vient du fichier config (il ne faut pas pouvoir avoir accès au mot de passe depuis github)
            smtp.login(FROM_EMAIL, MDP)

            # Envoie de l'email
            smtp.send_message(msg)
            print('Email correctement envoyé')
    except Exception as e:
        print(f'Error: {e}')
        return "error"