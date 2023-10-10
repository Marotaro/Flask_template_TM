from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db
from app.utils import *
from app.function import *

def on_create_owner(id_channel, owner, db):
            db.execute("INSERT INTO Permission (id_user_fk,id_channel_fk,type) VALUES (?, ?, 'owner')", (owner, id_channel))
            db.commit