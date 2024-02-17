from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app.db.db import get_db
from app.utils import *
from app.function.now import datenow
from app.function.themes import *
from app.function.permission import *
from app.function.image import upload_image
from app.function.token import *
from app.config import *

import os

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
        opento = request.form["opento"]
        owner = g.user["id_user"]
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
                "INSERT INTO Channel (name, date, opento, description) VALUES (?, ?, ?, ?)",
                (name, datenow(), opento, description),
            )
            db.commit()
            # récupere son id
            id_channel = db.execute(
                "SELECT id_channel FROM Channel ORDER BY id_channel DESC LIMIT 1;"
            ).fetchone()[0]
            # met le propriétaire par defaut
            add_permition(id_channel, owner, "owner", db)
            # créer les nouveaux themes si besoin et les lient avec la channel si theme est non nul
            if theme:
                new_theme(theme, db)
                link_theme_y(id_channel, theme, db)
                    # si image n'est pas dans la request, mettre la valeur par défaut
            

            upload_image("y",request.files['image'],id_channel,db)
                    
            return redirect(url_for("home.home"))
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
    channel_info = db.execute(
            "SELECT * FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE id_channel = ?", (id_channel,)
        ).fetchone()
    if channel_info['opento'] == "private"  and (not is_allowed(id_channel, g.user["id_user"], db)):
        return render_template("Y/not_permitted.html")
    else:
        channel_themes = db.execute(
            "SELECT name FROM Related_channel JOIN Themes On id_theme = id_theme_fk WHERE id_channel_fk = ? ",
            (id_channel,),
        ).fetchall()
        channel_normal_post =  db.execute(
            "SELECT text, image, username, id_post FROM Post JOIN User ON id_user = id_user_fk WHERE id_channel_fk = ? AND respond_to = -1",(id_channel,)
        ).fetchall()
        liked_post = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Likes WHERE id_user_fk = ?", (g.user['id_user'],)
        ).fetchall()]
        return render_template(
            "Y/see.html", channel_info=channel_info, channel_themes=channel_themes, channel_normal_post = channel_normal_post, liked_post = liked_post
        )
    
@y_bp.route("/get_comments/<int:id_post>", methods = ("GET","POST"))
@login_required
def get_comments(id_post):
    db = get_db()
    responds = []
    comments = db.execute(
            "SELECT text, image, username, id_post, respond_to FROM Post JOIN User ON id_user = id_user_fk WHERE respond_to = ?", (id_post,)
        ).fetchall()
    for comment in comments:
        respond = {
            'text' : comment[0],
            'image' : comment[1],
            'username' : comment[2],
            'id_post' : comment[3],
            'respond_to' : comment[4]
        }
        responds.append(respond)
    liked_resp_post = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Post JOIN Likes ON id_post= id_post_fk WHERE respond_to = ? AND Likes.id_user_fk = ?", (id_post,g.user['id_user'],)
        ).fetchall()]
    responds.append(liked_resp_post)
    return jsonify(responds)

    
# Route /y/browse
@y_bp.route("/browse", methods = ("GET", "POST"))
@login_required
def browse():
    # récuperer la base de données
    db = get_db()

    #récupérer les channels pour lesquelle l'utilisateur n'a pas de lien
    public_channel = db.execute(
        "SELECT * FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE opento = ?", ('public',)
    ).fetchall()

    return render_template(
        "Y/browse.html", public_channel=public_channel
    )

@y_bp.route("/invite/<int:id_channel>", methods = ("GET","POST"))
@login_required
def invite(id_channel):
    db = get_db()
    if not can_invite(id_channel, g.user['id_user'], ['owner','admin'], db):
        return render_template("Y/not_permitted.html")
    if request.method == "POST":
        expiration = request.form['expiration']
        token = create_token(g.user['id_user'],id_channel, int(expiration), 'channel', db)
        message = "lien copier dans le press papier"
        flash(f"{message}: {host}/y/join/{token}")
        return redirect(url_for("y.see", id_channel = id_channel))
    else:
        return render_template('Y/invite.html')
    

@y_bp.route("/join/<string:token>", methods = ("GET","POST"))
@login_required
def join(token):
    db = get_db()
    if valid_token(token,db):
        try:
            token_information = get_token(token,db)
            add_permition(token_information["id_channel_fk"], g.user['id_user'], "member", db)
            #flash([x for x in token_information])
            return redirect(url_for("y.see", id_channel = token_information["id_channel_fk"]))
        except:
            return redirect(url_for("home.home"))
    else:
        return render_template("Y/invite.html")