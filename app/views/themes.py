from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *


def correct_theme(theme_name):
    if theme_name == "":
        return None
    else:
        inter = theme_name.replace(" ","")
        inter = inter.lower()
        if len(inter) > 1 and inter[0] == "#":
            return inter.split("#")[1:]
        else:
            return "error"

    
def new_theme(themes,db):
    for theme in themes:
        test = db.execute('SELECT id_theme FROM Themes WHERE name = ?', (theme,)).fetchone()
        if test is None:
            db.execute("INSERT INTO Themes (name) VALUES (?)",(theme,))
            



def link_theme_y(id_y,themes,db):
    for theme in themes:
        id_theme = db.execute("SELECT id_theme FROM Themes WHERE name = ?", (theme,)).fetchone()
        db.execute("INSERT INTO Related_channel (id_channel_fk,id_theme_fk) VALUES (?,?)", (id_y,id_theme[0],))
        db.commit()


