from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import *
from app.function import *
from app.email import reset_message
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
        #on regarde si l'utilisateur est dans la base de donné grâce à son email
        id_user = db.execute("SELECT id_user FROM User WHERE email = ?",(email,)).fetchone()[0]
        if id_user != None:
            #on détruit par principe le token que l'utilisateur pourrait déjà avoir
            db.execute("DELETE FROM Token WHERE id_user_fk = ?", (id_user,))
            #générer le token
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            time = datetime.utcnow() + timedelta(minutes=5)
            #on sauvgarde le token dans une table nommé Token avec comme information le token, l'utilisateur au quel il est lié et la date avec l'heure précise en digit
            db.execute("INSERT INTO Token (token, id_user_fk, expiry) values (?, ?, ?)", (token, id_user, time.timestamp()))
            #code pour envoier le token par mail
            send_email(email,reset_message(token),"Réinitialisation du mot de passe")
        #code qui permet de supprimer les token expiré à chaque fois que quelqu'un fait une demande de token
        db.execute("DELETE FROM Token WHERE expiry > ?", (time.timestamp(),))
        db.commit()
        return render_template('password/confirm_request.html')
    else:
        return render_template('password/forgot_password.html')
    
@password_bp.route('/reset_password/<token>', methods=('GET','POST'))
def reset_password(token):
    db = get_db()
    #on contrôle que la demande existe
    existing_request = db.execute("SELECT id_user_fk, expiry FROM Token WHERE token = ?",(token,)).fetchone()
    if existing_request != None :
        #contrôle que la demande n'est pas expirée
        if datetime.utcnow().timestamp() < int(existing_request['expiry']):
            if request.method == 'POST':
                new_password = request.form['new_password']
                password_check = request.form['password_check']
                #contrôle que les deux mot de passe corresponde bien
                if new_password == password_check:
                    #on update le mot de passe de l'utilisateur
                    db.execute("UPDATE User SET password = ? WHERE id_user = ?",(generate_password_hash(new_password),existing_request['id_user_fk']))
                    #on suprime la demande
                    db.execute("DELETE FROM Token WHERE id_user_fk = ?", (existing_request['id_user_fk'],))
                    db.commit()
                    return redirect( url_for('auth.login'))
                else:
                    error = "not same"
                    flash(error)
                    return redirect( url_for('password.reset_password', token = token))
            else:
                return render_template('password/reset_password.html')
        else:
            error = "token exipered"
            flash(error)
            return redirect( url_for('password.forgot_password'))
    else:
        error = "request doesn't exist"
        flash(error)
        return redirect( url_for('password.forgot_passsword'))