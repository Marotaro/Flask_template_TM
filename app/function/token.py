import random
import string
from datetime import datetime, timedelta

def create_token(id_user, id_channel, duration, type ,db):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        time = datetime.utcnow()
        expiry = time + timedelta(minutes=duration)
        #supprétion des tokens expirés
        db.execute("DELETE FROM Token WHERE expiry < ?", (time.timestamp(),))
        #sauvegarde du token créé
        db.execute("INSERT INTO Token (token, id_user_fk, id_channel_fk, for, expiry) values (?, ?, ?, ?, ?)", (token, id_user, id_channel, type, expiry.timestamp()))
        db.commit()
        return token