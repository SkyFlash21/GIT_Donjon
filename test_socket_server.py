import jpysocket
import socket
import threading
import time
import struct
from serveur import *
import database
import re
import traceback

HEADER_SIZE = 4
Liste_Serveur = {}

"""
    # Ajouter un joueur
    joueur1_id = ajouter_joueur(conn, "Joueur1", "uuid1", "Serveur1")

    # Ajouter des mesures pour le joueur
    ajouter_mesure(conn, joueur1_id, "Donnees1")
    ajouter_mesure(conn, joueur1_id, "Donnees2")
    ajouter_mesure(conn, joueur1_id, "Donnees3")

    # Consulter la mesure la plus recente pour le joueur
    derniere_mesure_joueur1 = consulter_derniere_mesure(conn, joueur1_id)
    if derniere_mesure_joueur1:
        log("Derniere mesure pour le joueur 1 :")
        log(str(derniere_mesure_joueur1))
    else:
        log("Aucune mesure trouvee pour le joueur 1.")

    # Sauvegarder la base de donnees
    sauvegarder_base_de_donnees(conn)

    # Fermer la connexion a la base de donnees
    fermer_connexion(conn)
"""
def receive_message(connection):
    try:
        # Recevoir la taille du message à recevoir
        msg_size_data = b""
        while len(msg_size_data) < HEADER_SIZE:
            chunk = connection.recv(HEADER_SIZE - len(msg_size_data))
            if not chunk:
                return None
            msg_size_data += chunk
        msg_size = struct.unpack("!I", msg_size_data)[0]

        # Recevoir le message complet
        received_data = b""
        while len(received_data) < msg_size:
            chunk = connection.recv(msg_size - len(received_data))
            if not chunk:
                break
            received_data += chunk
        return received_data
    except:
        return None

def send_message(connection, message):
    # Envoyer la taille du message à envoyer
    msg_size = str(len(message)).zfill(HEADER_SIZE)
    connection.send(jpysocket.jpyencode(msg_size))

    # Envoyer le message complet
    print(f"Envoie d'un message de taille {msg_size}")
    connection.send(jpysocket.jpyencode(message))

def gerer_connexion(connection, address, uuid):
    
    database_connection,database_cursor = database.connecter_base_de_donnees()

    # Gérer la connexion d'un client
    print("Nouvelle connexion établie avec", address)

    # Envoyer un message de bienvenue au client
    send_message(connection, "Bienvenue ! Vous etes connecte au serveur Python.")
    send_message(connection, "Avant le debut de la loop")

    try:
        send_message(connection, "Debut de la loop")
        while True:
            # Recevoir les données du client
            msgrecv = receive_message(connection)
            if not msgrecv:
                # Si aucune donnée n'est reçue, la connexion est fermée
                connection.close()
                print(f"Aucunne donnée recue de {address}, fermeture de la connection")
                del Liste_Serveur[uuid]
                break

            # Décoder le message reçu
            msgrecv = str(msgrecv.decode())
            matches = re.findall(r'\[(.*?)\]', msgrecv[:90])
            if matches[0] == "Data_Joueur":
                print("Mise à jour de joueur recu.")
                data_len = len(matches[0]) + len(matches[1]) + len(matches[2]) + 6
                database.ajouter_ou_mettre_a_jour_joueur( matches[1], msgrecv[data_len:], matches[2], database_connection, database_cursor)
                send_message(connection, f"Message recu {len(msgrecv)}")
            elif matches[0] == "Request":
                print(f"Requette recu du serveur {address}")
                if matches[1] == "get_server":
                    send_message(connection, f"[Serveur_joueur][{matches[2]}][{database.recuperer_dernier_serveur(matches[2], database_connection, database_cursor)}]")
            else:
                print(msgrecv)

            # Envoyer une réponse au client
    except Exception:
        # Fermer la connexion lorsque la boucle est terminée
        connection.close()
        print(f"Connexion fermée avec {address} à cause d'une erreur.")
        print(traceback.format_exc())

        # Supprimer la connexion du dictionnaire
        del Liste_Serveur[uuid]

def verifier_connexions():
    while True:
        time.sleep(60)
        try:
            if len(Liste_Serveur) != 0:
                print("Vérification des connexions en cours...")
                for uuid, serveur in Liste_Serveur.items():
                    try:
                        send_message(serveur.connection, "getalive")
                    except:
                        print("La connexion avec ", uuid, serveur.addresse, "a été perdue.")
                        # Fermer la connexion et la supprimer du dictionnaire
                        serveur.connection.close()
                        del Liste_Serveur[serveur.uuid]
        except:
            print("Le thread de vérification des connections à rencontré une erreur.")

def main():
    global database_connection
    host = '127.0.0.1'  # Nom de l'hôte
    port = 12345  # Numéro de port
    s = socket.socket()  # Créer une socket
    s.bind((host, port))  # Lier le port et l'hôte
    s.listen(5)  # La socket est en écoute
    print("La socket est en écoute.")

    # Démarrer le thread de vérification des connexions
    thread_verification = threading.Thread(target=verifier_connexions)
    thread_verification.start()

    while True:
        # Accepter une nouvelle connexion
        connection, address = s.accept()
        print("Connecté à", address)

        # Ajouter la connexion au dictionnaire
        newserver = Serveur(str(connection.recv(32).decode()), address, connection)
        Liste_Serveur[newserver.uuid] = newserver

        # Gérer la connexion du client dans un thread séparé
        newserver.thread = threading.Thread(target=gerer_connexion, args=(newserver.connection, newserver.addresse, newserver.uuid))
        newserver.thread.start()

    # Fermer la socket lorsque la boucle est terminée
    s.close()
    print("Connexion fermée.")

if __name__ == '__main__':
    main()
