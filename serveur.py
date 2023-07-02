
class Serveur:
    def __init__(self,Nom_Serveur,Ip_serveur,Connection):
        self.uuid = Nom_Serveur
        self.addresse = Ip_serveur
        self.connection = Connection
        self.thread = None