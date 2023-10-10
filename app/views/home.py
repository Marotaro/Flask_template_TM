from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db

# Routes /...
home_bp = Blueprint('home', __name__)

# Route /
@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    # Affichage de la page principale de l'application
    return render_template('home/welcome.html')

@home_bp.route('/home', methods=('GET','POST'))
def home_page():
    
    db = get_db()

    g.mychannel = []
    # récupérer les channels
    ##celle ou l'utilisateur est l'owner
    id_channels = [row[0] for row in db.execute("SELECT id_channel_fk FROM Permission WHERE id_user_fk = ? AND  type = ?", (g.user['id_user'],"owner")).fetchall()]
    if id_channels:
        for id_channel in id_channels:
            g.mychannel.append(db.execute("SELECT * FROM Channel WHERE id_channel = ?", (id_channel,)).fetchall())
    # Affichage de la page d'un utilisateur connecté
    return render_template('home/index.html',id_channels=id_channels)

# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404
