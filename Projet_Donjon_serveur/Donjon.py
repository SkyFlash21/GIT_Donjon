import numpy as np
import Util,random,math,PathFinding

class Donjon:
    def __init__(self,Taille_Matrice,Nombre_de_Salle):
        self.matrices = np.zeros((Taille_Matrice[0], Taille_Matrice[1], Taille_Matrice[2])).astype(int) # Matrice du donjon, c'est ici que les salles vérifieront si elle peuvent se placer sans superposer une autre salle.
        self.taille = Taille_Matrice # Taille du donjon 
        self.Room_Type = {"1_etage":[],"2_etage":[],"hall":[]} # Type de salle (preset) classé par étage, une salle qui s'étend sur un étage auras l'index 0, deux étage : l'index 1. Les halls sont sur l'index 2

        self.salle_generer = [] # Liste 
        self.json_data = None # Data envoyé au serveur [non fini]
        self.Nombre_de_Salle = Nombre_de_Salle # Nombre de salle voulu pour le donjon au minimum et au maximum (tuple)

    def Get_disconnected_room(self,etage):
        disconnected_room_list = []
        for room in self.salle_generer[etage].values():
            for stage in range(len(room.connecteur_global)):
                for connector in room.connecteur_global[0]:
                    if connector[0] == etage+stage:
                        disconnected_room_list.append(room)

        return disconnected_room_list
    
    def Get_nearest_connected_room(self,origin_room):
        distance = None
        nearest_connected_room = None
        for room in self.salle_generer[origin_room.position[0]].values():
            temp_distance = math.dist(origin_room.position,room.position)
            # Si la distance n'est pas définie
            # Si la pièce est plus proches :
                # Si la piece est connecté
                # Si la piece est un hall ou un escalier qui a comme origine l'étage inférieur
            if distance == None or (temp_distance < distance and (len(room.connecteur_global[1]) != 0 or ( ("hall" in room.RoomType.name and len(room.connecteur_global[0]) != 0) or ("escalier" in room.RoomType.name and room.position[0] == (origin_room.position[0]-1) ) ))):
                if room not in origin_room.salle_connecter and origin_room != room and room not in origin_room.failed:
                    distance = temp_distance
                    nearest_connected_room = room
        return nearest_connected_room

    def Get_Distance_from_center(self,center,etage):
        distance_list = []
        for room in self.salle_generer[etage].values():
            distance = math.dist(center.position, room.position)
            if distance > 0:
                distance_list.append((distance, room))
        
        distance_list.sort(key=lambda x: x[0])  # Tri des salles par distance croissante
        
        sorted_rooms = [room for _, room in distance_list]  # Création de la liste triée des salles
        
        return sorted_rooms
    
    def Connect_rooms(self,roomA,roomB):
        # On identifie les connecteurs valide, ensuite on connecte les deux salles

        # Sélection du connecteur dans la roomA et roomB
        Aindex = 0
        if len(roomA.connecteur_global[0]) == 0:
            Aindex = 1
        Bindex = 0
        if len(roomB.connecteur_global[0]) == 0:
            Bindex = 1

        distance = None
        selected_connector = []
        for Aconnecteur in roomA.connecteur_global[Aindex]:
            for Bconnecteur in roomB.connecteur_global[Bindex]:
                temp_distance = math.dist(Aconnecteur,Bconnecteur)
                if (distance == None or temp_distance < distance) and not Util.Compare_tuple(Aconnecteur,Bconnecteur):
                    distance = temp_distance
                    selected_connector = (Aconnecteur,Bconnecteur)
        
        if selected_connector != [] :
            return Aindex,Bindex,selected_connector
        else:
            return None,None,None