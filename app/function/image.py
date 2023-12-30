from app.db.db import get_db
from app.config import *
import os

def upload_image(destination,image,fk_id,db):
    table, fk_row_name, folder, short_folder = ("Image_channel","id_channel_fk",UPLOAD_FOLDER_Y, SHORT_FOLDER_Y) if destination == "y" else (("Image_user","id_user_fk",UPLOAD_FOLDER_USER, SHORT_FOLDER_USER) if destination == "user" else ("Image_post","id_post_fk",UPLOAD_FOLDER_POST, SHORT_FOLDER_POST))
    try:
        lastidimage = int(db.execute(f"SELECT MAX(id_image) FROM {table}").fetchone()[0]) + 1
    except:
        lastidimage = 0
    try:
        if image and image.filename != '':
            extension = os.path.splitext(image.filename)[1]
            image.filename = str(lastidimage) + extension
            image.save(os.path.join(folder, image.filename))
            link = short_folder + str(image.filename)
            db.execute(f"INSERT INTO {table} ({fk_row_name}, location) VALUES (?,?)", (fk_id, link),)
        else:
            db.execute(f"INSERT INTO {table} ({fk_row_name}) VALUES (?)", (fk_id,),)
    except:
        db.execute(f"INSERT INTO {table} ({fk_row_name}) VALUES (?)", (fk_id,),)
    db.commit()
    