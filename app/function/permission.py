from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *

def on_create_owner(id_channel, owner, db):
    db.execute("INSERT INTO Permission (id_user_fk,id_channel_fk,type) VALUES (?, ?, 'owner')", (owner, id_channel))
    db.commit()

def allowed(id_channel, id_user, db):
    opento = db.execute('SELECT opento FROM Channel WHERE id_channel = ?', (id_channel,)).fetchone()
    authorisation = db.execute('SELECT * FROM Permission WHERE id_channel_fk = ? AND id_user_fk = ?', (id_channel, id_user)).fetchone()
    try:
        if authorisation['type'] == "ban":
            return False
        else:
            if opento == "private":
                if authorisation is None or authorisation['type'] not in ["owner","admin","member"]:
                    return False
                else:
                    return True
            else:
                return True
    except:
        return False
            
def can_invite(id_channel, id_user, permission_needed,db):
    if allowed(id_channel, id_user, db):
        authorisation = db.execute('SELECT * FROM Permission WHERE id_channel_fk = ? AND id_user_fk = ?', (id_channel, id_user)).fetchone()
        if authorisation['type'] not in permission_needed:
            return False
        else:
            return True
    else:
        return False