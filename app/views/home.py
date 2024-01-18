from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.function.get_channel import *
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


    # récupérer les channels
    ##celle ou l'utilisateur est l'owner
    mychannels = get_y_by_user(g.user['id_user'], "owner", db)
    memberchannels = get_y_by_user(g.user['id_user'], "member", db)
    # Affichage de la page d'un utilisateur connecté
    return render_template("home/index.html", mychannels=mychannels,memberchannels=memberchannels)


# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route("/<path:text>", methods=["GET", "POST"])
def not_found_error(text):
    return render_template("home/404.html"), 404
