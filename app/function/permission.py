from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *

def perimssion_already_existe(id_channel, id_user, db):
    return db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Permission WHERE id_user_fk = ? and id_channel_fk = ?) THEN 1 ELSE 0 END",(id_user, id_channel)).fetchone()[0]

def add_permition(id_channel, id_user, type, db):
    if not perimssion_already_existe(id_channel, id_user, db):
        db.execute("INSERT INTO Permission (id_user_fk,id_channel_fk,type) VALUES (?, ?, ?)", (id_user, id_channel, type))
        db.commit()
    
def is_allowed(id_channel, id_user, db):
    opento = db.execute('SELECT opento FROM Channel WHERE id_channel = ?', (id_channel,)).fetchone()
    authorisation = db.execute("WITH MyCTE AS (SELECT type FROM Permission WHERE id_user_fk = ? AND id_channel_fk = ?) SELECT CASE WHEN EXISTS (SELECT * FROM MyCTE) THEN (SELECT type FROM MyCTE) ELSE 0 END AS result;",(id_user,id_channel)).fetchone()[0]
    try:
        if authorisation == "ban":
            return False
        else:
            if opento == "private" and (authorisation not in ["owner", "admin", "member"]):
                return False
            else:
                return True
    except:
        return False
    
def can_invite(id_channel, id_user, permission_needed,db):
    if is_allowed(id_channel, id_user, db):
        authorisation = db.execute('SELECT * FROM Permission WHERE id_channel_fk = ? AND id_user_fk = ?', (id_channel, id_user)).fetchone()
        if authorisation['type'] not in permission_needed:
            return False
        else:
            return True
    else:
        return False