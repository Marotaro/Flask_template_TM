from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app.db.db import get_db, close_db
from app.utils import *
from app.function.now import datenow
from app.function.themes import *
from app.function.permission import *
from app.function.image import *
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
            close_db()
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
            close_db()
            return redirect(url_for("home.home"))
        else:
            error = "No Y's name given"
            flash(error)
            close_db()
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
        close_db()
        return render_template("Y/not_permitted.html")
    else:
        channel_themes = db.execute(
            "SELECT name FROM Related_channel JOIN Themes On id_theme = id_theme_fk WHERE id_channel_fk = ? ",
            (id_channel,),
        ).fetchall()
        channel_normal_post =  db.execute(
            "SELECT text, Image_post.location, username, Image_user.location AS usericon , id_post, Post.id_user_fk FROM Post JOIN User ON id_user = Post.id_user_fk LEFT JOIN Image_post ON id_post_fk = id_post JOIN Image_user ON Post.id_user_fk = Image_user.id_user_fk WHERE id_channel_fk = ? AND respond_to = -1;",(id_channel,)
        ).fetchall()
        liked_post = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Likes WHERE id_user_fk = ?", (g.user['id_user'],)
        ).fetchall()]
        favorited_posts = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Favorit WHERE id_user_fk = ?", (g.user['id_user'],)
        ).fetchall()]
        close_db()
        return render_template(
            "Y/see.html", channel_info=channel_info, channel_themes=channel_themes, channel_normal_post = channel_normal_post, liked_post = liked_post, favorited_posts = favorited_posts
        )
    
@y_bp.route("/get_comments/<int:id_post>", methods = ("GET","POST"))
@login_required
def get_comments(id_post):
    db = get_db()
    responds = []
    comments = db.execute(
            "SELECT text, Image_post.location, username, Image_user.location AS usericon , id_post, Post.id_user_fk, respond_to FROM Post JOIN User ON id_user = Post.id_user_fk LEFT JOIN Image_post ON id_post_fk = id_post JOIN Image_user ON Post.id_user_fk = Image_user.id_user_fk WHERE respond_to = ?", (id_post,)
        ).fetchall()
    for comment in comments:
        if comment[1] == None:
            image = 'vide'
        else:
            image = comment[1]
        respond = {
            'text' : comment[0],
            'location' : g.host + '/'+ image,
            'username' : comment[2],
            'usericon' : comment[3],
            'id_post' : comment[4],
            'id_user' : comment[5],
            'respond_to' : comment[6],
        }
        responds.append(respond)
    liked_resp_post = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Post JOIN Likes ON id_post= id_post_fk WHERE respond_to = ? AND Likes.id_user_fk = ?", (id_post,g.user['id_user'],)
        ).fetchall()]
    favorited_resp_post = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Post JOIN Favorit ON id_post= id_post_fk WHERE respond_to = ? AND Favorit.id_user_fk = ?", (id_post,g.user['id_user'],)
        ).fetchall()]
    responds.append(liked_resp_post)
    responds.append(favorited_resp_post)
    close_db()
    return jsonify(responds)

    
# Route /y/browse
@y_bp.route("/browse", methods = ("GET", "POST"))
@login_required
def browse():
    # récuperer la base de données
    db = get_db()

    #récupérer les channels pour lesquelle l'utilisateur n'a pas de lien
    public_channels = db.execute(
        "SELECT * FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE opento = ? ORDER BY RANDOM() LIMIT 5", ('public',)
    ).fetchall()

    themes_random = db.execute("Select * FROM Themes ORDER BY RANDOM() LIMIT 7").fetchall()
    close_db()
    return render_template(
        "Y/browse.html", public_channels=public_channels, themes_random = themes_random
    )

@y_bp.route("/search/<string:search_request>", methods = ("GET","POST"))
@login_required
def search(search_request):
    db = get_db()
    try:

        elements = search_request.split("%20")
        if search_request != '|empty|':
            message = False
            themes = [str("%"+x[1:]+"%").lower() for x in elements if "#" == x[0]]
            names = [str("%"+x[1:]+"%").lower() for x in elements if "&" == x[0] ]
            both = [str("%"+x+"%").lower() for x in elements if "&" != x[0] and "#" != x[0]]

            themes += both
            names += both

            channels_by_names = [channel for sublist in [[c for c in db.execute("SELECT id_channel, Channel.name, location FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE opento = 'public' AND LOWER(name) LIKE ?", (b,)).fetchall()] for b in names] for channel in sublist]
            channels_by_themes = [channel for sublist in [[c for c in db.execute("SELECT id_channel, Channel.name, location FROM Channel JOIN Related_channel ON Related_channel.id_channel_fk = Channel.id_channel JOIN Themes ON Related_channel.id_theme_fk = Themes.id_theme JOIN Image_channel ON Image_channel.id_channel_fk = Channel.id_channel WHERE  opento = 'public' AND LOWER(Themes.name) LIKE ?", (b,)).fetchall()] for b in themes] for channel in sublist if channel not in channels_by_names]
            channels = list(set(channels_by_names + channels_by_themes))
            if channels == []:
                message = True
        else:
            channels = []
            message = True  
        responds = [0] * len(channels)

        for i, channel in enumerate(channels):
            respond = {
                'idChannel' : channel[0],
                'name' : channel[1],
                'location' : channel[2],
            }
            responds[i] = respond
        close_db()
        return jsonify(responds, message)
   
    except:
        message = True
        channels = [x for x in db.execute( "SELECT id_channel, Channel.name, location FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE opento = ?", ('public',) ).fetchall()]
        responds = [0] * len(channels)
        for i, channel in enumerate(channels):
            respond = {
                'idChannel' : channel[0],
                'name' : channel[1],
                'location' : channel[2],
            }
            responds[i] = respond
        close_db()
        return jsonify(responds, message)

@y_bp.route("/invite/<int:id_channel>/<int:duration>", methods = ("GET","POST"))
@login_required
def invite(id_channel, duration):
    db = get_db()
    if not can_invite(id_channel, g.user['id_user'], ['owner','admin'], db):
        close_db()
        return jsonify({'respond': "you don't have the permission to do that"})
    else:
        try:
            token = create_token(g.user['id_user'],id_channel, int(duration), 'channel', db)
            close_db()
            return jsonify({'respond': f"{g.host}/y/join/{token}"})
        except:
            close_db()
            return jsonify({'respond': "can't create link"})
    

@y_bp.route("/join/<string:token>", methods = ("GET","POST"))
@login_required
def join(token):
    db = get_db()
    if valid_token(token,db):
        try:
            token_information = get_token(token,db)
            add_permition(token_information["id_channel_fk"], g.user['id_user'], "member", db)
            #flash([x for x in token_information])
            close_db()
            return redirect(url_for("y.see", id_channel = token_information["id_channel_fk"]))
        except:
            close_db()
            return redirect(url_for("home.home"))
    else:
        close_db()
        return render_template("Y/invite.html")
    
@y_bp.route("/leave/<int:id_channel>", methods = ("GET","POST"))
@login_required
def leave(id_channel):
    db = get_db()
    try:
        db.execute("DELETE FROM Permission WHERE id_user_fk = ? AND id_channel_fk = ?", (g.user['id_user'], id_channel,))
        db.commit()
        close_db()
        return redirect(url_for("home.home"))
    except:
        close_db()
        return redirect(url_for("y.about", id_channel = id_channel))
    


@y_bp.route("/about/<int:id_channel>", methods = ("GET","POST"))
@login_required
def about(id_channel):
    db = get_db()
    channel_info = db.execute(
        "SELECT * FROM Channel JOIN Image_channel ON id_channel = id_channel_fk WHERE id_channel = ?", (id_channel,)
    ).fetchone()
    if channel_info['opento'] == "private"  and (not is_allowed(id_channel, g.user["id_user"], db)):
        close_db()
        return render_template("Y/not_permitted.html")
    else:
        if request.method == "POST":
            # Récupérer les informations de la requet HTTP
            name = request.form["name"]
            description = request.form["bio"]
            print(request.form['themes'])
            theme = correct_theme(request.form["themes"])
            if theme == "error":
                error = "Incorrect Theme name. Try <#theme_name> or leave it empty"
                flash(error)
                close_db()
                return redirect(url_for("y.about", id_channel = id_channel))
            # si name n'est pas nul rajouter une nouvelle ligne à Channel sinon retourner le message d'erreur
            if name:
                # crée la ligne de la nouvelle channel
                db.execute(
                    "UPDATE Channel SET name = ?, description = ? WHERE id_channel = ?",
                    (name, description, id_channel,)
                )
                db.commit()

                # créer les nouveaux themes si besoin et les lient avec la channel si theme est non nul
                unlink_theme_y(id_channel, db)
                if theme:
                    new_theme(theme, db)
                    link_theme_y(id_channel, theme, db)
                        # si image n'est pas dans la request, mettre la valeur par défaut
    
                update_image("y",request.files['image'],id_channel,db)
                close_db()
                return redirect(url_for("y.about", id_channel = id_channel))
            else:
                error = "No Y's name given"
                flash(error)
                close_db()
                return redirect(url_for("y.about", id_channel = id_channel))
            
        else:
            owners = db.execute("SELECT id_user, username FROM Permission JOIN User ON id_user_fk = id_user WHERE id_channel_fk = ? AND type = 'owner'", (id_channel,)).fetchall()
            admins = db.execute("SELECT id_user, username FROM Permission JOIN User ON id_user_fk = id_user WHERE id_channel_fk = ? AND type = 'admin'", (id_channel,)).fetchall()
            members = db.execute("SELECT id_user, username FROM Permission JOIN User ON id_user_fk = id_user WHERE id_channel_fk = ? AND type = 'member'", (id_channel,)).fetchall()
            bans = db.execute("SELECT id_user, username FROM Permission JOIN User ON id_user_fk = id_user WHERE id_channel_fk = ? AND type = 'ban'", (id_channel,)).fetchall()
            channel_themes = db.execute(
                "SELECT name FROM Related_channel JOIN Themes On id_theme = id_theme_fk WHERE id_channel_fk = ? ",
                (id_channel,),
            ).fetchall()
            nb_participants = db.execute("SELECT count(id_user_fk) FROM Permission WHERE id_channel_fk = ? AND type != 'ban'",(id_channel,)).fetchone()[0]
            nb_posts = db.execute("SELECT count(id_post) FROM Post WHERE id_channel_fk = ?", (id_channel,)).fetchone()[0]
            close_db()
            return render_template("Y/about.html", channel_info = channel_info, owners = owners, admins = admins, members = members, bans = bans ,channel_themes = channel_themes, nb_participants = nb_participants, nb_posts = nb_posts)

@y_bp.route("/delete/<int:id_channel>", methods = ("GET","POST"))
@login_required
def delete(id_channel):
    db = get_db()
    permission = db.execute("SELECT type FROM Permission WHERE id_user_fk = ? AND id_channel_fk = ?", (g.user['id_user'], id_channel,)).fetchone()[0] 
    if permission == "owner":
        try:
            delete_image("y", id_channel, db)
        except:
            pass
        db.execute("DELETE FROM Channel WHERE id_channel = ?", (id_channel,))
        db.commit()
        close_db()
        return redirect(url_for("home.home"))
    else:
        flash("Vous n'êtes pas authorisé à faire cela")
        close_db()
        return render_template("home/404.html")
    


@y_bp.route("/change_role/<int:id_channel>/<int:id_user>/<string:type>", methods = ("GET","POST"))
@login_required
def change_role(id_channel, id_user, type):
    db = get_db()
    permission = db.execute("SELECT type FROM Permission WHERE id_user_fk = ? AND id_channel_fk = ?", (g.user['id_user'], id_channel,)).fetchone()[0] 
    if permission == "owner":
        db.execute("UPDATE Permission SET type = ? WHERE id_channel_fk = ? AND id_user_fk = ?", (type, id_channel, id_user))
        db.commit()
        close_db()
        return jsonify({"role": type, "user": id_user})
    else:
        flash("Vous n'êtes pas authorisé à faire cela")
        close_db()
        return render_template("home/404.html")