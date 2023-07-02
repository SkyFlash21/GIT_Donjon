import sqlite3
from datetime import datetime
import os

# Connexion a la base de donnees
def connecter_base_de_donnees():
    conn = sqlite3.connect('ma_base_de_donnees.db')
    charger_joueurs(conn)  # Charge les joueurs deja presents
    return conn

# Verification de l'existence d'une table dans la base de donnees
def table_existe(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

# Creation des tables dans la base de donnees
def creer_tables(conn):
    if not table_existe(conn, 'Joueurs'):
        create_joueurs_table_query = '''
            CREATE TABLE Joueurs (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Pseudo TEXT,
                UUID TEXT,
                DernierServeur TEXT
            )
        '''
        conn.execute(create_joueurs_table_query)
        log("Table 'Joueurs' creee dans la base de donnees.")

    if not table_existe(conn, 'DonneesJeu'):
        create_donneesjeu_table_query = '''
            CREATE TABLE DonneesJeu (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                AutresDonnees TEXT
            )
        '''
        conn.execute(create_donneesjeu_table_query)
        log("Table 'DonneesJeu' creee dans la base de donnees.")

    if not table_existe(conn, 'MesuresJoueur'):
        create_mesuresjoueur_table_query = '''
            CREATE TABLE MesuresJoueur (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                IDJoueur INTEGER,
                IDDonnees INTEGER,
                DateMesure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (IDJoueur) REFERENCES Joueurs(ID),
                FOREIGN KEY (IDDonnees) REFERENCES DonneesJeu(ID)
            )
        '''
        conn.execute(create_mesuresjoueur_table_query)
        log("Table 'MesuresJoueur' creee dans la base de donnees.")

# Charger les joueurs deja presents dans la base de donnees
def charger_joueurs(conn):
    try:
        select_joueurs_query = '''
            SELECT ID, Pseudo, UUID, DernierServeur FROM Joueurs
        '''
        cursor = conn.cursor()
        cursor.execute(select_joueurs_query)
        joueurs = cursor.fetchall()
        for joueur in joueurs:
            joueur_id, pseudo, uuid, dernier_serveur = joueur
            log(f"Joueur charge depuis la base de donnees. ID du joueur : {joueur_id}")
    except:
        log(f"La table joueur n'existe pas, ou une autre erreur a ete rencontre.")
        
# Ajout d'un joueur a la base de donnees
def ajouter_joueur(conn, pseudo, uuid, dernier_serveur):
    select_joueur_query = '''
        SELECT ID FROM Joueurs WHERE Pseudo = ? AND UUID = ?
    '''
    cursor = conn.cursor()
    cursor.execute(select_joueur_query, (pseudo, uuid))
    joueur = cursor.fetchone()
    if joueur:
        log("Le joueur existe deja dans la base de donnees.")
        return joueur[0]  # Retourne l'ID du joueur existant

    insert_joueur_query = '''
        INSERT INTO Joueurs (Pseudo, UUID, DernierServeur)
        VALUES (?, ?, ?)
    '''
    cursor.execute(insert_joueur_query, (pseudo, uuid, dernier_serveur))
    joueur_id = cursor.lastrowid
    conn.commit()
    log(f"Joueur ajoute a la base de donnees. ID du joueur : {joueur_id}")
    return joueur_id

# Ajout d'une mesure pour un joueur donne
def ajouter_mesure(conn, joueur_id, donnees):
    select_joueur_query = '''
        SELECT ID FROM Joueurs WHERE ID = ?
    '''
    cursor = conn.cursor()
    cursor.execute(select_joueur_query, (joueur_id,))
    joueur = cursor.fetchone()
    if not joueur:
        raise ValueError("Joueur avec l'ID {} non trouve.".format(joueur_id))

    insert_donnees_query = '''
        INSERT INTO DonneesJeu (AutresDonnees)
        VALUES (?)
    '''
    cursor.execute(insert_donnees_query, (donnees,))
    donnees_id = cursor.lastrowid

    insert_mesure_query = '''
        INSERT INTO MesuresJoueur (IDJoueur, IDDonnees)
        VALUES (?, ?)
    '''
    cursor.execute(insert_mesure_query, (joueur_id, donnees_id))
    mesure_id = cursor.lastrowid

    conn.commit()
    log(f"Mesure ajoutee pour le joueur avec l'ID : {joueur_id}, ID de mesure : {mesure_id}")
    return mesure_id

# Consultation de la derniere mesure pour un joueur donne
def consulter_derniere_mesure(conn, joueur_id):
    select_query = '''
        SELECT J.ID, J.Pseudo, J.UUID, J.DernierServeur, D.AutresDonnees, MJ.DateMesure
        FROM Joueurs J
        INNER JOIN MesuresJoueur MJ ON J.ID = MJ.IDJoueur
        INNER JOIN DonneesJeu D ON MJ.IDDonnees = D.ID
        WHERE J.ID = ?
        ORDER BY MJ.DateMesure DESC
        LIMIT 1
    '''
    cursor = conn.cursor()
    cursor.execute(select_query, (joueur_id,))
    resultat = cursor.fetchone()
    return resultat

# Consultation d'une mesure specifique par son ID
def consulter_mesure_par_id(conn, mesure_id):
    select_query = '''
        SELECT J.ID, J.Pseudo, J.UUID, J.DernierServeur, D.AutresDonnees, MJ.DateMesure
        FROM Joueurs J
        INNER JOIN MesuresJoueur MJ ON J.ID = MJ.IDJoueur
        INNER JOIN DonneesJeu D ON MJ.IDDonnees = D.ID
        WHERE MJ.ID = ?
    '''
    cursor = conn.cursor()
    cursor.execute(select_query, (mesure_id,))
    resultat = cursor.fetchone()
    return resultat

# Obtenir le dernier serveur visite par un joueur
def obtenir_dernier_serveur(conn, joueur_id):
    select_query = '''
        SELECT DernierServeur
        FROM Joueurs
        WHERE ID = ?
    '''
    cursor = conn.cursor()
    cursor.execute(select_query, (joueur_id,))
    dernier_serveur = cursor.fetchone()
    return dernier_serveur[0] if dernier_serveur else None

# Sauvegarder la base de donnees
def sauvegarder_base_de_donnees(conn):
    # Create a backup directory if it doesn't exist
    backup_dir = 'backup/'
    os.makedirs(backup_dir, exist_ok=True)

    # Generate the backup filename with the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = f'{backup_dir}ma_base_de_donnees_backup_{current_datetime}.db'

    # Perform the backup
    backup_conn = sqlite3.connect(backup_file)
    conn.backup(backup_conn)
    backup_conn.close()

    log("La base de donnees a ete sauvegardee dans le fichier : {}".format(backup_file))

# Fermer la connexion a la base de donnees
def fermer_connexion(conn):
    conn.close()
    log("Connexion a la base de donnees fermee.")

# Fonction pour enregistrer les actions dans le fichier log
def log(message):
    log_file = 'log.txt'
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'{current_datetime} - {message}\n'
    with open(log_file, 'a') as f:
        f.write(log_entry)