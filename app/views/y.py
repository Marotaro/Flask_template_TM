from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *

# Routes /y/...
y_bp = Blueprint('y', __name__, url_prefix='/y')

@y_bp.route('/create_y', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':

        # Récupérer les informations de la requet HTTP
        name = request.form['name']
        description = request.form ['bio']
#        owner = g.user['id_user']
#        theme_name = request.form['theme']
        # si icon n'a pas de valeur mettre la valeur par défaut
        if request.form['icon'] == None:
            icon = "default"
        else:
            icon = request.form['icon']

        # récupérer la base de donné
        db = get_db()
#        
#        # si theme_name a une valeur
#        if theme_name:
#            # chercher si le theme existe déjà
#            theme=db.execute("Select * FROM Themes WHERE name = ?", (theme_name)).fetchone()
#            # s'il existe pas le rajouter dans la table theme
#            if theme == None:
#                db.execute("INSERT INTO Themes (name) VALUES (?)",(theme_name))
#                db.commit()
#            theme_id = 
        # si name n'est pas nul rajouter une nouvelle ligne à Channel sinon retourner le message d'erreur
        if name:
            db.execute("INSERT INTO Channel (name, date, description, icon) VALUES (?, ?, ?, ?)", (name, datenow(), description, icon))
            db.commit()
            return render_template('/home/index.html')
        else:
            error = "No Y's name given"
            flash(error)
            return redirect(url_for("y.create"))
        

        


    else:
        return render_template('Y/create.html')