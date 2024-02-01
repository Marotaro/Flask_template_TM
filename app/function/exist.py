def exist(table, columne_name, data, db):
    return db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM ? WHERE ? = ?)THEN 1 ELSE 0 END", (table, columne_name, data,)).fetchone()[0]


#pas encore trouver comment faire fonctionner
def exist_multiple_argument(table, list_columne_name, list_data, db):
    return db.execute("SELECT CASE WHEN EXISTS (SELECT * FROM ? WHERE ? = ?)THEN 1 ELSE 0 END", (table, columne_name, data,)).fetchone()[0]