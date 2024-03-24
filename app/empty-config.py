import os

#clef de chiffrement
SECRET_KEY = "sdg554ASDF45asdfsASF5"
#nom de la base de donné
DATABASE = "Name.db"

#dossiers
WORKING_DIR = os.path.normpath(os.getcwd() + r"\APP\\")
#chemin des dossiers (les dossier doivent exister)
SHORT_FOLDER_USER = "static/image/user_icon/"
SHORT_FOLDER_Y = "static/image/y_icon/"
SHORT_FOLDER_POST = "static/image/user_icon/"

#adresse de l'hebergeur
host = r"http://127.0.00:5000"
#informations du server de mail
MAIL_HOST = r"smtp.office365.com"
PORT = 587
#informations du compte pour envoyer des mails
UTIL_MAIL = r"exemple.exp@outlook.com" 
MDP = r"SK.f_75!"

#toutes les variables définies au dessus ne sont des exemples, il faut les compléter avec les informations que vous allez utiliser.
#vous pouvez grader le chemin des dossiers, veillez juste à avoir les dossiers.
