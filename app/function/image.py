from app.db.db import get_db
from app.config import WORKING_DIR, host, SHORT_FOLDER_POST, SHORT_FOLDER_USER, SHORT_FOLDER_Y
from werkzeug.utils import secure_filename
import os

def upload_image(destination,image,fk_id,db):
    table, fk_row_name, short_folder = ("Image_channel","id_channel_fk", SHORT_FOLDER_Y) if destination == "y" else (("Image_user","id_user_fk", SHORT_FOLDER_USER) if destination == "user" else ("Image_post","id_post_fk", SHORT_FOLDER_POST))
    try:
        lastidimage = int(db.execute(f"SELECT MAX(id_image) FROM {table}").fetchone()[0]) + 1
    except:
        lastidimage = 0
    try:
        if image and image.filename != '':
            extension = os.path.splitext(image.filename)[1]
            image.filename = secure_filename(str(lastidimage) + extension)
            image.save(os.path.join(WORKING_DIR + short_folder, image.filename))
            link = short_folder + str(image.filename)
            db.execute(f"INSERT INTO {table} ({fk_row_name}, location) VALUES (?,?)", (fk_id, link),)
        else:
            db.execute(f"INSERT INTO {table} ({fk_row_name}, location) VALUES (?,?)", (fk_id,os.path.join(short_folder, "default.png")),)
    except:
        db.execute(f"INSERT INTO {table} ({fk_row_name}, location) VALUES (?,?)", (fk_id,os.path.join(short_folder, "default.png")),)
    db.commit()
    