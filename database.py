import sqlite3
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Fonction pour se connecter à la base de données
def connecter_base_de_donnees():
    conn = sqlite3.connect('joueurs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS joueurs (
            uuid TEXT PRIMARY KEY,
            data TEXT,
            dernier_serveur TEXT,
            transfert_valider INTEGER DEFAULT 0
        )
    ''')
    logging.info("Connexion à la base de données établie")
    return conn, c

# Fonction pour ajouter ou mettre à jour un joueur dans la base de données
def ajouter_ou_mettre_a_jour_joueur(uuid, data, dernier_serveur, transfert_valider, conn, c):
    c.execute('SELECT uuid FROM joueurs WHERE uuid = ?', (uuid,))
    result = c.fetchone()
    if result:
        # UUID exists, update the player's data
        c.execute('UPDATE joueurs SET data = ?, dernier_serveur = ?, transfert_valider = ? WHERE uuid = ?', (data, dernier_serveur, transfert_valider, uuid))
        conn.commit()
        logging.info("Joueur mis à jour avec succès. UUID: %s", uuid)
    else:
        # UUID doesn't exist, insert a new player
        c.execute('INSERT INTO joueurs (uuid, data, dernier_serveur, transfert_valider) VALUES (?, ?, ?, ?)', (uuid, data, dernier_serveur, transfert_valider))
        conn.commit()
        logging.info("Joueur ajouté avec succès. UUID: %s", uuid)

# Fonction pour récupérer le data d'un joueur
def recuperer_data(uuid, conn, c):
    c.execute('SELECT data FROM joueurs WHERE uuid = ?', (uuid,))
    result = c.fetchone()
    if result:
        logging.info("Données récupérées pour le joueur. UUID: %s", uuid)
        return result[0]
    else:
        logging.warning("Impossible de récupérer les données. UUID: %s", uuid)
        return None

# Fonction pour récupérer le dernier serveur accédé par un joueur
def recuperer_dernier_serveur(uuid, conn, c):
    c.execute('SELECT dernier_serveur FROM joueurs WHERE uuid = ?', (uuid,))
    result = c.fetchone()
    if result:
        logging.info("Dernier serveur récupéré pour le joueur. UUID: %s", uuid)
        return result[0]
    else:
        logging.warning("Impossible de récupérer le dernier serveur. UUID: %s", uuid)
        return None

# Fonction pour récupérer l'état de transfert validé par un joueur
def recuperer_transfert_valider(uuid, conn, c):
    c.execute('SELECT transfert_valider FROM joueurs WHERE uuid = ?', (uuid,))
    result = c.fetchone()
    if result:
        logging.info("État de transfert récupéré pour le joueur. UUID: %s", uuid)
        return bool(result[0])
    else:
        logging.warning("Impossible de récupérer l'état de transfert. UUID: %s", uuid)
        return None

# Fonction pour récupérer toutes les données d'un joueur
def recuperer_donnees_joueur(uuid, conn, c):
    c.execute('SELECT * FROM joueurs WHERE uuid = ?', (uuid,))
    result = c.fetchone()
    if result:
        logging.info("Données récupérées pour le joueur. UUID: %s", uuid)
        return {
            'uuid': result[0],
            'data': result[1],
            'dernier_serveur': result[2],
            'transfert_valider': bool(result[3])
        }
    else:
        logging.warning("Impossible de récupérer les données. UUID: %s", uuid)
        return None
