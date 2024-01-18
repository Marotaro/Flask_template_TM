from app.db.db import get_db
from app.utils import *
from app.function.now import datenow
from app.function.themes import *
from app.function.token import *
from app.config import *

def get_y_by_user(id_user, perimssion, db):
    return db.execute("SELECT id_user_fk, type, id_channel, name, Channel.date, description, id_image, location FROM Permission JOIN Channel ON Permission.id_channel_fk = Channel.id_channel JOIN Image_channel ON Permission.id_channel_fk = Image_channel.id_channel_fk WHERE id_user_fk = ? AND type = ?", (id_user, perimssion)).fetchall()