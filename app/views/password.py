from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import *
from app.function.send import *
from app.function.email import reset_message
from app.function.token import *
import random
import string
from datetime import datetime, timedelta

password_bp = Blueprint('password', __name__, url_prefix='/password')

#changer le mot de passe d'un utilisateur
@password_bp.route('/change_password', methods=('GET','POST'))
@login_required
def changepassword():
    if request.method == 'POST':
        new_password = request.form['new_password']
        password_check = request.form['password_check']
        old_password = request.form['old_password']
        if new_password == password_check:
            if check_password_hash(g.user['password'],old_password):
                db = get_db()
                db.execute("UPDATE User SET password = ? WHERE id_user = ?",(generate_password_hash(new_password),g.user['id_user']))
                db.commit()
                return render_template('user/profile.html')
            else:
                error = "old password incorrect"
                flash(error)
                return redirect(url_for("password.changepassword"))
        else:
            error = "new password not the same"
            flash(error)
            return redirect(url_for("password.changepassword"))
    else:
        return render_template('password/changepassword.html')
    
@password_bp.route('/forgot_password', methods=('GET','POST'))
def forgot_password():
    if request.method == 'POST':
        #émail retourner par un Form
        email = request.form['email']
        db = get_db()
        #on regarde si l'utilisateur est dans la base de donné grâce à son email sinon on renvoie un message d'erreur
        try:
            id_user = db.execute("SELECT id_user FROM User WHERE email = ?",(email,)).fetchone()[0]
            token = create_token(id_user, None, 10, "password", db)
            if send_email(email,reset_message(token),"Réinitialisation du mot de passe") == "error":
                error = "Oups, il y a eu un problème lors de l'envoie du mail "
                flash(error)
                return render_template('password/forgot_password.html')
            return render_template('password/confirm_request.html')
        except:
            error = "Cet utilisateur n'existe pas"
            flash(error)
            return render_template('password/forgot_password.html')
    else:
        return render_template('password/forgot_password.html')
    
@password_bp.route('/reset_password/<token>', methods=('GET','POST'))
def reset_password(token):
    db = get_db()
    #on contrôle que la demande existe
    if valid_token(token,db) :
        token_information = get_token(token,db)
        if request.method == 'POST':
            new_password = request.form['new_password']
            password_check = request.form['password_check']
            #contrôle que les deux mot de passe corresponde bien
            if new_password == password_check:
                #on update le mot de passe de l'utilisateur
                db.execute("UPDATE User SET password = ? WHERE id_user = ?",(generate_password_hash(new_password),token_information['id_user_fk']))
                #on suprime la demande
                db.execute("DELETE FROM Token WHERE id_user_fk = ?", (token_information['id_user_fk'],))
                db.commit()
                return redirect( url_for('auth.login'))
            else:
                error = "not same"
                flash(error)
                return redirect( url_for('password.reset_password', token = token))
        else:
            return render_template('password/reset_password.html')
    else:
        error = "request doesn't exist or is expired"
        flash(error)
        return redirect( url_for('password.forgot_password'))