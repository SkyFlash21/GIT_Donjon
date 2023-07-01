import socket

HEADERSIZE = 10

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((socket.gethostname(), 1234))

def send_all_message(message):
    message = f"{len(message):<{HEADERSIZE}}"+message
    connection.sendall(bytes(message,"utf-8"))

def close_connection():
    send_all_message("close_connection")
    connection.close()

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = connection.recv(16)
        if new_msg:
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"Réception du message en cours : {round((min(msglen,len(full_msg))/msglen)*100)}%")

        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ""
