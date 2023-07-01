import jpysocket
import socket
import time
from _thread import *
ServerSideSocket = socket.socket()
host = "127.0.0.1"
port = 12345
Client_list = []
HEADERSIZE = 10

# Section relative au test des connections (envoie des get_alive packet)
def check_all_client(Client_list): 
    while True:
        if len(Client_list) != 0:
            print(f"[Thread] Envoie du packet is_alive à {len(Client_list)} clients")
            for client_tuple in Client_list:
                client = client_tuple[0]
                try:
                    client.send(jpysocket.jpyencode("checka"))
                except error:
                    print(f"Un client à été déconnecté brutalement.")
                    Client_list.remove(client)
        time.sleep(5)

# Section relative à l'envoie et la reception des messages (modification pour abaisser le buffer)
def send_message(connection,message):
    message = f"{len(message):<{HEADERSIZE}}"+message
    connection.send(jpysocket.jpyencode(message))

# Section relative au client
def receive_message(connection):
    # Recevoir l'en-tête contenant la taille du message
    header_size = 10  # Taille fixe de l'en-tête
    try:
        header = connection.recv(header_size)
        message_size = int(jpysocket.jpydecode(header).strip())  # Convertir l'en-tête en entier
        print(f"header : [{jpysocket.jpydecode(header)}], message size: [{message_size}]")

        # Recevoir le corps du message en plusieurs morceaux
        message = b""
        chunk_size = 4096  # Taille maximale fixe pour chaque morceau
        print(len(message) < message_size,len(message),message_size)
        while len(message) < message_size:
            remaining_bytes = message_size - len(message) + 2
            chunk = connection.recv(min(chunk_size, remaining_bytes))
            message += chunk
            print(f"Réception: [{jpysocket.jpydecode(chunk)}] {len(message)} {message_size}")
        print(jpysocket.jpydecode(message))
        return jpysocket.jpydecode(message)
    except:
        return "close_connection"

def client_handler(connection,address,Client_list):
    send_message(connection,'[Helios] Connection réussi.')
    while True:
        message = receive_message(connection)
        if message == 'close_connection':
            print("Fermeture de la connection")
            Client_list.remove((connection,address))
            break
        reply = f'Server: {message}'
        send_message(connection,reply)
    connection.close()

# Section relative au serveur
def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connection accepté: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client,address,Client_list, ))
    Client_list.append((Client,address))

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print(f'Le serveur à été démmaré sur le port {port}...')
    ServerSocket.listen()
    start_new_thread(check_all_client, (Client_list, ))
    while True:
        accept_connections(ServerSocket)

start_server(host, port)