import sqlite3, hashlib
from math import pi, sin, cos, atan2, sqrt
def ouvrir_connexion():
    cnx = None
    try:
        cnx = sqlite3.connect('ThronExpress/db/thronDB.db')
    except BaseException as e:
        print(e)
    return cnx

def db_identification(resultat):
    #hachage du mot de passe
    password = hashlib.sha256()
    password.update(bytes(resultat['password'], 'utf-8'))
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * \
    FROM Utilisateurs\
    WHERE username = ? AND password = ?",\
    (resultat['login'], password.hexdigest()))
    rows = cur.fetchall()
    cnx.close()
    return rows

def addUser(uuid, username, name, phone, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    
    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    cur.execute("SELECT * FROM User WHERE phone = ?", (phone,))
    rows = cur.fetchall()
    if len(rows) != 0:
        return False

    cur.execute("INSERT INTO User VALUES (?, ?, ?, ?, ?, ?, ?)",(str(uuid), \
                    username, name, phone, password.hexdigest(), False, None))
    cnx.commit()
    cnx.close()
    return True


def getUser(uuid):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM User WHERE UUID = ?", (uuid,))
    rows = cur.fetchall()
    cnx.close()
    return rows[0] # retourne UN tuple (sinon renvoie une liste de 1 tuple donc c'est useless)

def log_in(username, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password.hexdigest()))
    rows = cur.fetchall()
    cnx.close()
    return rows

def getNearbyToilets(lat, lon, threshold):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    cur.execute("SELECT * FROM Bathroom")
    rows = cur.fetchall()
    cnx.close()

    result = []
    for row in rows:
        distance = calc_distance(lat, lon, row[4], row[5])
        if distance <= threshold:
            result.append(row)

    return result

def calc_distance(lat1, lon1, lat2, lon2):
    R = 6371e3
    phi1 = lat1 * pi/180
    phi2 = lat2 * pi/180

    deltaPhi = (lat2-lat1) * pi/180
    deltaLambda = (lon2 - lon1) * pi/180

    a = sin(deltaPhi/2) * sin(deltaPhi/2) + \
    cos(phi1) * cos(phi2) * \
    sin(deltaLambda/2) * sin(deltaLambda/2)

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c

def changePassword(uuid, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    print("old psswrd: ", password.hexdigest())
    print("uid: ", uuid)

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("UPDATE User SET password = ? WHERE UUID = ?", (password.hexdigest(), uuid))
    cnx.commit()
    cnx.close()