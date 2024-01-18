import random
import string
from datetime import datetime, timedelta

def delete_expired_token(db):
        time = datetime.utcnow()
        db.execute("DELETE FROM Token WHERE expiry < ?", (time.timestamp(),))
        db.commit()

def create_token(id_user, id_channel, duration, type ,db):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        time = datetime.utcnow()
        expiry = time + timedelta(minutes=duration)
        #supprétion des tokens expirés
        delete_expired_token(db)
        #sauvegarde du token créé
        db.execute("INSERT INTO Token (token, id_user_fk, id_channel_fk, for, expiry) values (?, ?, ?, ?, ?)", (token, id_user, id_channel, type, expiry.timestamp()))
        db.commit()
        return token

def valid_token(token, db):
        delete_expired_token(db)
        return db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Token WHERE token = ?)THEN 1 ELSE 0 END", (token,)).fetchone()[0]

def get_token(token, db):
        return db.execute("SELECT * FROM Token where token = ?", (token,)).fetchone()