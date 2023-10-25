from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *
from app.views.themes import *
from app.views.permission import *

# Routes /y/...
y_bp = Blueprint("y", __name__, url_prefix="/y")


# Routes /y/create
@y_bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        # Récupérer les informations de la requet HTTP
        name = request.form["name"]
        description = request.form["bio"]
        owner = g.user["id_user"]
        # si icon n'a pas de valeur mettre la valeur par défaut
        if request.form["icon"] == None:
            icon = "default"
        else:
            icon = request.form["icon"]
        # récupérer la base de donné
        db = get_db()
        theme = correct_theme(request.form["themes"])
        if theme == "error":
            error = "Incorrect Theme name. Try <#theme_name> or leave it empty"
            flash(error)
            return redirect(url_for("y.create"))
        # si name n'est pas nul rajouter une nouvelle ligne à Channel sinon retourner le message d'erreur
        if name:
            # crée la ligne de la nouvelle channel
            db.execute(
                "INSERT INTO Channel (name, date, description, icon) VALUES (?, ?, ?, ?)",
                (name, datenow(), description, icon),
            )
            db.commit()
            # récupere son id
            id_channel = db.execute(
                "SELECT id_channel FROM Channel ORDER BY id_channel DESC LIMIT 1;"
            ).fetchone()[0]
            # met le propriétaire par defaut
            on_create_owner(id_channel, owner, db)
            # créer les nouveaux themes si besoin et les lient avec la channel si theme est non nul
            if theme:
                new_theme(theme, db)
                link_theme_y(id_channel, theme, db)
            return redirect(url_for("home.home_page"))
        else:
            error = "No Y's name given"
            flash(error)
            return redirect(url_for("y.create"))
    else:
        return render_template("Y/create.html")


# Route /y/see
@y_bp.route("/see/<int:id_channel>", methods=("GET", "POST"))
@login_required
def see(id_channel):
    # récupérer la base de données
    db = get_db()

    if allowed(id_channel, g.user["id_user"], db) == False:
        return render_template("Y/not_permitted.html")
    else:
        channel_info = db.execute(
            "SELECT * FROM Channel WHERE id_channel = ?", (id_channel,)
        ).fetchone()
        channel_themes = db.execute(
            "SELECT name FROM Related_channel JOIN Themes On id_theme = id_theme_fk WHERE id_channel_fk = ? ",
            (id_channel,),
        ).fetchall()
        channel_post =  db.execute(
            "SELECT text, image, username FROM Post JOIN User ON id_user = id_user_fk WHERE id_channel_fk = ?",(id_channel,)
        ).fetchall()
        return render_template(
            "Y/see.html", channel_info=channel_info, channel_themes=channel_themes, channel_post = channel_post
        )
        
