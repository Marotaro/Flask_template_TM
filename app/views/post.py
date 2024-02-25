from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app.db.db import get_db
from app.utils import *
from app.function.now import *
from app.function.exist import *
from app.function.permission import *
from app.function.image import *


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/create_post/<id_channel>/<respondto>', methods = ('GET','POST'), endpoint = 'create_post')
@login_required
def create_post(id_channel,respondto):
    if request.method == 'POST':
        #récupérer les informations de la request HTTP 
        text = request.form['textarea']
        image = request.files['image']

        #récupérer la base de données
        db = get_db()
        if text:
            db.execute("INSERT INTO Post (id_channel_fk, id_user_fk, date, respond_to, text) VALUES (?, ?, ?, ?, ?)", (id_channel, g.user['id_user'], datenow(), int(respondto), text,))
            db.commit()
            add_permition(id_channel, g.user['id_user'], 'member', db)
            if image:
                id_post = db.execute(
                    "SELECT id_post FROM Post ORDER BY id_post DESC LIMIT 1;"
                ).fetchone()[0]
                upload_image("post",image, id_post, db )
            return redirect(url_for("y.see", id_channel = id_channel))
        else:
            return redirect(url_for('create_post', id_channel = id_channel, respondto = respondto))
    else:
        return render_template('post/create.html', id_channel = id_channel)
    
@post_bp.route('/like_post/<id_post>', methods = ["GET"])
@login_required
def like_post(id_post):
    db = get_db()
    post = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Post WHERE id_post= ?)THEN 1 ELSE 0 END", (id_post,)).fetchone()[0]
    if post:
        liked = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Likes WHERE id_user_fk = ? AND id_post_fk = ?)THEN 1 ELSE 0 END", (g.user["id_user"], id_post,)).fetchone()[0]
        if liked:
            db.execute("DELETE FROM Likes WHERE id_user_fk = ? AND id_post_fk = ?", (g.user["id_user"], id_post,))
            liked = False
        else:
            db.execute("INSERT INTO Likes (id_user_fk, id_post_fk) VALUES (?,?)",(g.user["id_user"], id_post,))
            liked = True
        db.commit()
        return jsonify({"liked": liked}, 400)
    else:
        return jsonify({"error": "La publication n'existe pas"}, 400)
    
@post_bp.route('/delete_post_from_channel/<id_channel>/<id_post>', methods = ["GET","Post"])
@login_required
def delete_post_from_channel(id_channel,id_post):
    db = get_db()
    creator = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Post WHERE id_user_fk = ? AND id_post = ? )THEN 1 ELSE 0 END", (g.user["id_user"], id_post,)).fetchone()[0]
    if creator:
        db.execute("DELETE FROM Post WHERE id_post = ?",(id_post,))
        db.execute("DELETE FROM Post WHERE respond_to = ?",(id_post,))
        db.commit()
        delete_image("post", id_post, db)
        return redirect(url_for('y.see', id_channel = id_channel))
    else:
        flash("vous n'est pas autorisé à faire ça")
        return render_template('home/404.html')
    
@post_bp.route('/modify_post_from_channel/<id_channel>/<id_post>', methods = ["GET","Post"])
@login_required
def modify_post_from_channel(id_channel,id_post):
    db = get_db()
    creator = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Post WHERE id_user_fk = ? AND id_post = ? )THEN 1 ELSE 0 END", (g.user["id_user"], id_post,)).fetchone()[0]
    if creator:
        if request.method == 'POST':
            text = request.form['textarea']


            if text:
                db.execute("UPDATE Post SET text = ?WHERE id_post = ?", (text, id_post,))
                db.commit()
                update_image("post", request.files['image'], id_post, db)
                return redirect(url_for("y.see", id_channel = id_channel))
            else:
                return redirect(url_for('modify_post_from_channel', id_channel = id_channel, id_post = id_post))
        else:
            text = db.execute("SELECT text, location FROM Post LEFT JOIN Image_post ON id_post = id_post_fk WHERE id_post = ?", (id_post,)).fetchone()
            return render_template('post/create.html', modify = text, id_channel = id_channel)
    else:
        flash("vous n'est pas autorisé à faire ça")
        return render_template('home/404.html')
    

@post_bp.route('/delete_post/<id_post>', methods = ["GET","Post"])
@login_required
def delete_post(id_post):
    db = get_db()
    creator = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Post WHERE id_user_fk = ? AND id_post = ? )THEN 1 ELSE 0 END", (g.user["id_user"], id_post,)).fetchone()[0]
    if creator:
        db.execute("DELETE FROM Post WHERE id_post = ?",(id_post,))
        db.execute("DELETE FROM Post WHERE respond_to = ?",(id_post,))
        db.commit()
        delete_image("post", id_post, db)
        return jsonify({"result": "ok"}, 400)
    else:
        flash("vous n'est pas autorisé à faire ça")
        return render_template('home/404.html')
    
@post_bp.route('/modify_post/<id_post>', methods = ["GET","Post"])
@login_required
def modify_post(id_post):
    db = get_db()
    creator = db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Post WHERE id_user_fk = ? AND id_post = ? )THEN 1 ELSE 0 END", (g.user["id_user"], id_post,)).fetchone()[0]
    if creator:
        if request.method == 'POST':
            text = request.form['textarea']


            if text:
                db.execute("UPDATE Post SET text = ? WHERE id_post = ?", (text, id_post,))
                db.commit()
                update_image("post", request.files['image'], id_post, db)
                return redirect(url_for("user.show_posts"))
            else:
                return redirect(url_for('modify_post', id_post = id_post))
        else:
            text = db.execute("SELECT text, location FROM Post LEFT JOIN Image_post ON id_post = id_post_fk WHERE id_post = ?", (id_post,)).fetchone()
            return render_template('post/create.html', modify = text)
    else:
        flash("vous n'est pas autorisé à faire ça")
        return render_template('home/404.html')