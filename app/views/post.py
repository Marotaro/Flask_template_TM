from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app.db.db import get_db
from app.utils import *
from app.function.now import *
from app.function.exist import *


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/create_post/<id_channel>/<respondto>', methods = ('GET','POST'), endpoint = 'create_post')
@login_required
def create_post(id_channel,respondto):
    if request.method == 'POST':
        #récupérer les informations de la request HTTP 
        text = request.form['textarea']
        image = request.form['image']

        #récupérer la base de données
        db = get_db()
        if text:
            db.execute("INSERT INTO Post (id_channel_fk, id_user_fk, date, respond_to, text, image) VALUES (?, ?, ?, ?, ?, ?)", (id_channel, g.user['id_user'], datenow(), int(respondto), text, image))
            db.commit()
            return redirect(url_for("y.see", id_channel = id_channel))
        else:
            return redirect(url_for('create_post', id_channel = id_channel, respondto = respondto))
    else:
        return render_template('post/create.html')
    
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
            image = request.form['image']

            if text:
                db.execute("UPDATE Post SET text = ?, image = ? WHERE id_post = ?", (text, image, id_post,))
                db.commit()
                return redirect(url_for("y.see", id_channel = id_channel))
            else:
                return redirect(url_for('modify_post_from_channel', id_channel = id_channel, id_post = id_post))
        else:
            text = db.execute("SELECT text FROM Post WHERE id_post = ?", (id_post,)).fetchone()[0]
            return render_template('post/create.html', modify = text)
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
            image = request.form['image']

            if text:
                db.execute("UPDATE Post SET text = ?, image = ? WHERE id_post = ?", (text, image, id_post,))
                db.commit()
                return redirect(url_for("user.show_posts"))
            else:
                return redirect(url_for('modify_post', id_post = id_post))
        else:
            text = db.execute("SELECT text FROM Post WHERE id_post = ?", (id_post,)).fetchone()[0]
            return render_template('post/create.html', modify = text)
    else:
        flash("vous n'est pas autorisé à faire ça")
        return render_template('home/404.html')