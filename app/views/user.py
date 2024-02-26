from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.function.get_channel import *
from app.function.image import update_image
from app.utils import *

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    db = get_db()
    y_info = db.execute("SELECT (SELECT COUNT(*) FROM Channel JOIN Permission ON Channel.id_channel = Permission.id_channel_fk WHERE Permission.id_user_fk = ? AND Permission.type = 'owner' ) AS nb_created_y, ( SELECT COUNT(*) FROM Channel JOIN Permission ON Channel.id_channel = Permission.id_channel_fk WHERE Permission.id_user_fk = ? AND (Permission.type = ('owner') OR Permission.type = ('member')) ) AS nb_member_y ", (g.user['id_user'],g.user['id_user'],)).fetchone()
    post_info = db.execute("SELECT ( SELECT COUNT(*) FROM Post WHERE id_user_fk = ? ) AS nb_posted_post", (g.user['id_user'],)).fetchone()
    like_info = db.execute("SELECT ( SELECT COUNT(*) FROM Likes WHERE id_user_fk = ? ) AS nb_liked_post, ( SELECT COUNT(*) FROM Likes JOIN Post ON id_post = id_post_fk WHERE Post.id_user_fk = ? ) AS nb_like_post", (g.user['id_user'],g.user['id_user'],)).fetchone()
    favorit_info = db.execute("SELECT ( SELECT COUNT(*) FROM Favorit WHERE id_user_fk = ? ) AS nb_favorited_post, ( SELECT COUNT(*) FROM Favorit JOIN Post ON id_post = id_post_fk WHERE Post.id_user_fk = ? ) AS nb_favorit_post", (g.user['id_user'],g.user['id_user'],)).fetchone()
    return render_template('profil/user/profile.html', y_info = y_info, post_info = post_info, like_info = like_info, favorit_info = favorit_info )

@user_bp.route('/show_posts', methods=('GET', 'POST'))
@login_required 
def show_posts():
    db = get_db()
    posts = db.execute("SELECT Post.id_post, Post.text, FromUser.username AS RespondTo, Channel.name AS ChannelName FROM Post LEFT JOIN Post AS RespondToPost ON Post.respond_to = RespondToPost.id_post LEFT JOIN User AS FromUser ON RespondToPost.id_user_fk = FromUser.id_user JOIN Channel ON Channel.id_channel = Post.id_channel_fk WHERE Post.id_user_fk = ?", (g.user['id_user'],)).fetchall()
    liked_posts = [x[0] for x in db.execute(
            "SELECT id_post_fk FROM Likes WHERE id_user_fk = ?", (g.user['id_user'],)
        ).fetchall()]
    return render_template('profil/user/posts.html', posts = posts, liked_posts = liked_posts)

@user_bp.route('/show_ys', methods=('GET', 'POST'))
@login_required
def show_ys(): 
    db = get_db()
    # récupérer les channels
    ##celle ou l'utilisateur est l'owner
    myys = get_y_by_user(g.user['id_user'], "owner", db)
    memberys = get_y_by_user(g.user['id_user'], "member", db)
    # Affichage de la page d'un utilisateur connecté
    return render_template("profil/user/ys.html", myys=myys,memberys=memberys)

@user_bp.route('/show_likes', methods=('GET', 'POST'))
@login_required
def show_likes():
    db = get_db()
    likes =  db.execute("SELECT Asdf.id_post, Asdf.text, Creator.username AS CreatorName, FromUser.username AS RespondTo, Channel.name AS ChannelName FROM Likes JOIN Post AS Asdf ON Asdf.id_post = Likes.id_post_fk LEFT JOIN Post AS RespondToPost ON Asdf.respond_to = RespondToPost.id_post LEFT JOIN User AS FromUser ON RespondToPost.id_user_fk = FromUser.id_user JOIN Channel ON Channel.id_channel = Asdf.id_channel_fk JOIN User AS Creator ON Creator.id_user = Asdf.id_user_fk WHERE Likes.id_user_fk = ?", (g.user['id_user'],)).fetchall()
    return render_template("profil/user/likeds.html", likes=likes)

@user_bp.route('/show_favorits', methods=('GET', 'POST'))
@login_required
def show_favorits():
    db = get_db()
    favorits =  db.execute("SELECT Asdf.id_post, Asdf.text, Creator.username AS CreatorName, FromUser.username AS RespondTo, Channel.name AS ChannelName FROM Favorit JOIN Post AS Asdf ON Asdf.id_post = Favorit.id_post_fk LEFT JOIN Post AS RespondToPost ON Asdf.respond_to = RespondToPost.id_post LEFT JOIN User AS FromUser ON RespondToPost.id_user_fk = FromUser.id_user JOIN Channel ON Channel.id_channel = Asdf.id_channel_fk JOIN User AS Creator ON Creator.id_user = Asdf.id_user_fk WHERE Favorit.id_user_fk = ?", (g.user['id_user'],)).fetchall()
    return render_template("profil/user/favorits.html", favorits=favorits)

@user_bp.route('/show_parametre', methods=('GET', 'POST'))
@login_required
def show_parametre():
    if request.method == 'POST':
        #try:
            new_username = request.form['username']
            image = request.files['image']

            db = get_db()

            db.execute("UPDATE User SET username = ? WHERE id_user = ?", (new_username, g.user['id_user']))
            db.commit()
            update_image('user', image, g.user['id_user'], db)
            return redirect(url_for("user.show_parametre"))
        #except:
        #    return redirect(url_for("user.show_parametre"))
    else:
        return render_template("profil/user/parametre.html")