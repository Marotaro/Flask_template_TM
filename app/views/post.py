from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *


post_bp = Blueprint('post', __name__, url_prefix='/post')


@post_bp.route('/create_post/<id_channel>/<respondto>', methods = ('GET','POST'), endpoint = 'create_post')
def create_post(id_channel,respondto):
    if request.method == 'POST':
        #récupérer les informations de la request HTTP 
        text = request.form['text']
        image = request.form['image']

        #récupérer la base de données
        db = get_db()
        if text:
            db.execute("INSERT INTO Post (id_channel_fk, id_user_fk, date, respond_to, text, image) VALUES (?, ?, ?, ?, ?, ?)", (id_channel, g.user['id_user'], datenow(), respondto, text, image))
            db.commit()
            return redirect(url_for("y.see", id_channel = id_channel))
        else:
            return redirect(url_for('create_post', id_channel = id_channel, respondto = respondto))
    else:
        return render_template('post/create.html')
        

