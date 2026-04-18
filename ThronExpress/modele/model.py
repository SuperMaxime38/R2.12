import sqlite3, hashlib, time
def ouvrir_connexion():
    cnx = None
    try:
        cnx = sqlite3.connect('Projet/db/bd_youtube.db')
    except BaseException as e:
        print(e)
    return cnx

def research(query, userID = None):

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Videos WHERE title LIKE ? OR author LIKE ?", (f"%{query}%", f"%{query}%"))
    rows = cur.fetchall()
    cnx.close()

    return getVideoTable(rows, userID)

def db_identification(resultat):
    #hachage du mot de passe
    password = hashlib.sha256()
    password.update(bytes(resultat['password'], 'utf-8'))
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * \
    FROM Utilisateurs\
    WHERE pseudo = ? AND password = ?",\
    (resultat['login'], password.hexdigest()))
    rows = cur.fetchall()
    cnx.close()
    return rows

def addUser(uuid, pseudo, mail, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    
    cnx = ouvrir_connexion()
    cur = cnx.cursor()

    cur.execute("SELECT * FROM Utilisateurs WHERE adr_mail = ?", (mail,))
    rows = cur.fetchall()
    if len(rows) != 0:
        return False

    cur.execute("INSERT INTO Utilisateurs VALUES (?, ?, ?, ?)",(uuid, \
                    mail, pseudo, password.hexdigest()))
    cnx.commit()
    cnx.close()
    return True


def getUser(uuid):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM Utilisateurs WHERE userID = ?", (uuid,))
    rows = cur.fetchall()
    cnx.close()
    return rows[0] # retourne UN tuple (sinon renvoie une liste de 1 tuple donc c'est useless)

def changePassword(uuid, passwrd):
    password = hashlib.sha256()
    password.update(bytes(passwrd, 'utf-8'))

    print("old psswrd: ", password.hexdigest())
    print("uid: ", uuid)

    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("UPDATE Utilisateurs SET password = ? WHERE userID = ?", (password.hexdigest(), uuid))
    cnx.commit()
    cnx.close()

def getUserFromMail(mail):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT userID FROM Utilisateurs WHERE adr_mail = ?", (mail,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return None

    return rows[0][0]

def getMailFromUser(userID):
    cnx = ouvrir_connexion()
    cur = cnx.cursor()
    cur.execute("SELECT adr_mail FROM Utilisateurs WHERE userID = ?", (userID,))
    rows = cur.fetchall()
    cnx.close()

    if len(rows) == 0:
        return None

    return rows[0][0]
