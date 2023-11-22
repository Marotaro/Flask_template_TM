from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *

# Routes /...
home_bp = Blueprint("home", __name__)


# Route /
@home_bp.route("/", methods=("GET", "POST"))
def landing_page():
    # Affichage de la page principale de l'application
    return render_template("home/welcome.html")


@home_bp.route("/home", methods=("GET", "POST"))
@login_required
def home_page():
    db = get_db()

    mychannels = []
    # récupérer les channels
    ##celle ou l'utilisateur est l'owner
    id_channels = [
        row[0]
        for row in db.execute(
            "SELECT id_channel_fk FROM Permission WHERE id_user_fk = ? AND  type = ?",
            (g.user["id_user"], "owner"),
        ).fetchall()
    ]
    for id_channel in id_channels:
        channel_details = db.execute(
            "SELECT * FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE id_channel = ?",
            (id_channel,),
        ).fetchone()

        if channel_details:
            mychannels.append(channel_details)
    # Affichage de la page d'un utilisateur connecté
    return render_template("home/index.html", mychannels=mychannels)


# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route("/<path:text>", methods=["GET", "POST"])
def not_found_error(text):
    return render_template("home/404.html"), 404
