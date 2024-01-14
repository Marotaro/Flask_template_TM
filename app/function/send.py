#smtplib est une librairie rajoutée, il faut donc la téléchargée 
import smtplib
from app.config import MDP, MAIL_HOST, PORT, UTIL_MAIL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, message, subject):
    #Information général de l'envoie
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = UTIL_MAIL
    msg['To'] = to_email
    msg['Cc'] = UTIL_MAIL
    msg['Bcc'] = UTIL_MAIL

    #Message peut être une simple chaine de caractères pour ceci il suffit de remplacer MIMEText(message,'plain')
    #ici il s'agit dans fichier html
    msg.attach(MIMEText(message, 'html'))
    try:
        with smtplib.SMTP(MAIL_HOST, port = PORT) as smtp:
            #Connection au serveur smtp
            smtp.ehlo()
            smtp.starttls()
            #MDP vient du fichier config (il ne faut pas pouvoir avoir accès au mot de passe depuis github)
            smtp.login(UTIL_MAIL, MDP)

            # Envoie de l'email
            smtp.send_message(msg)
            print('Email correctement envoyé')
    except Exception as e:
        print(f'Error: {e}')
        return "error"