import numpy as np
import Util,random,math,PathFinding
import Outil_generation
import json

class Donjon:
    def __init__(self,Taille_Matrice,Nombre_de_Salle):
        self.matrices = np.zeros((Taille_Matrice[0], Taille_Matrice[1], Taille_Matrice[2])).astype(int) # Matrice du donjon, c'est ici que les salles vérifieront si elle peuvent se placer sans superposer une autre salle.
        self.taille = Taille_Matrice # Taille du donjon 
        self.Room_Type = {"1_etage":[],"2_etage":[],"hall":[]}
        self.salle_generer = [] # Liste 
        self.json_data = None # Data envoyé au serveur [non fini]
        self.Nombre_de_Salle = Nombre_de_Salle # Nombre de salle voulu pour le donjon au minimum et au maximum (tuple)
        self.time = None

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
            if distance == None or (temp_distance < distance and (len(room.connecteur_global[1]) != 0 or ( ("hall" == room.RoomType.name[-4:] and len(room.connecteur_global[0]) != 0) or ("escalier" in room.RoomType.name and room.position[0] == (origin_room.position[0]-1) ) ))):
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
    
    def is_dungeon_valid(self):
        Donjon_valide = True
        for etage in range(len(self.matrices)):
            # On trouve l'origine de l'étage (salle qui fait escalier entre deux étage)
            origin_etage = None
            if etage != 0:
                for room in self.salle_generer[etage-1].values():
                    if len(room.matrice) == 2:
                        origin_etage = room
            elif etage == 0:
                for room in self.salle_generer[etage].values():
                    if "hall" == room.RoomType.name[-4:]:
                        origin_etage = room

            ordered = self.Get_Distance_from_center(origin_etage,etage) # Tri des salles en foncion de la distance

            tentative_discconnected = 0
            disconnected = self.Get_disconnected_room(etage)
            while disconnected != []:
                tentative_discconnected += 1
                if tentative_discconnected > 100:
                    break
                if len(disconnected) == 1:
                    if "hall" == disconnected[0].RoomType.name[-4:]:
                        break
                for roomA in ordered:
                    if roomA in disconnected :
                        nearest_connected_room = self.Get_nearest_connected_room(roomA)
                        if nearest_connected_room == None:
                            break
                        
                        Aindex,Bindex,connector = self.Connect_rooms(roomA,nearest_connected_room)

                        if connector != None:
                            path_betwen_point = PathFinding.find_shortest_path(self.matrices,connector[0],connector[1],{3:1,0:3})
                            if path_betwen_point != None:
                                roomA.salle_connecter.append(nearest_connected_room)
                                nearest_connected_room.salle_connecter.append(roomA)
                                if Aindex == 0:
                                    roomA.connecteur_global[Aindex].remove(connector[0])
                                    roomA.connecteur_global[1].append(connector[0])
                                else:
                                    roomA.connecteur_global[Aindex].remove(connector[0])

                                if Bindex == 0:
                                    nearest_connected_room.connecteur_global[Bindex].remove(connector[1])
                                    nearest_connected_room.connecteur_global[1].append(connector[1])
                                else:
                                    nearest_connected_room.connecteur_global[Bindex].remove(connector[1])
                                    
                                for point in path_betwen_point:
                                    self.matrices[point] = 3
                            else:
                                roomA.failed.append(nearest_connected_room)
                                nearest_connected_room.failed.append(roomA)
                        else:
                            roomA.failed.append(nearest_connected_room)
                            nearest_connected_room.failed.append(roomA)
                disconnected = self.Get_disconnected_room(etage)  
        for etage in self.matrices:
            if 5 in etage:
                Donjon_valide = False

        return Donjon_valide

    
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
    
    def Generate(self,stage_escalier):
        is_hall_generated = False

        for iy,y in enumerate(self.matrices):
            historique = []
            self.salle_generer.append({})
            global_shape = self.matrices.shape


            # Placement des salles dans la matrices
            nombre_de_salle = random.randint(self.Nombre_de_Salle[0],self.Nombre_de_Salle[1])
            for i in range(nombre_de_salle):

                # Géneration du hall ou des escaliers
                if is_hall_generated == False:
                    selected_room = random.choice(self.Room_Type["hall"]).GenerateRoom()
                else:
                    if stage_escalier > 0 and iy != len(self.matrices)-1:
                        selected_room = random.choice(self.Room_Type["2_etage"]).GenerateRoom()
                        stage_escalier-=1
                    else:
                        selected_room = random.choice(self.Room_Type["1_etage"]).GenerateRoom()

                
                # Définition de la rotation de la salle
                
                selected_room.Rotate_Room(selected_room.rotation)
                if selected_room.RoomType.name[-4:] == "hall":
                    selected_room.rotation = 0

                """ A REFAIRE
                    # Définition du fait que la salle soit en miroir ou non
                    if selected_room.miror:
                        for i,stage in enumerate(selected_room.matrice):
                            selected_room.matrice[i] = np.flip(selected_room.matrice[i], axis=1)
                """
                rotated_shape = selected_room.matrice.shape
                for tentative in range(50):
                    direction = [(1,0),(-1,0),(0,1),(0,-1)]
                    valide = True
                    position = (iy,random.randint(0,global_shape[1]-rotated_shape[1]),random.randint(0,global_shape[2]-rotated_shape[2]))
                    for posy in range(rotated_shape[0]):
                        if valide == False : break
                        for posx in range(rotated_shape[1]):
                            if valide == False : break
                            for posz in range(rotated_shape[2]):
                                if valide == False : break
                                # Test de superposition
                                if not self.matrices[(position[0]+posy,position[1]+posx,position[2]+posz)] + selected_room.matrice[posy,posx,posz] in [0,1,3,5]:
                                    valide = False

                                # Test d'accessibilité des connecteurs
                                if selected_room.matrice[posy,posx,posz] == 5:
                                    # Exclusion des bordures
                                    if posx+position[1] == global_shape[1]-1 or posx+position[1] == 0:
                                        valide = False
                                    elif posz+position[2] == global_shape[2]-1 or posz+position[2] == 0:
                                        valide = False
                                        
                    # Vérification que on bouche pas un connecteur

                    if valide:
                        rotated_shape = selected_room.matrice.shape
                        matrice_copy = self.matrices.copy()
                        matrice_copy[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                        if Outil_generation.verif_room_connector(matrice_copy):
                            if 5 not in self.matrices[position[0]:position[0]+rotated_shape[0],max(0,position[1]-1):min(global_shape[1],position[1]+rotated_shape[1]+2),max(0,position[2]-1):min(global_shape[2],position[2]+rotated_shape[2]+2)]:
                                selected_room.position = position
                                selected_room.Update_connecteur_global()
                                self.salle_generer[iy][selected_room.position] = selected_room
                                self.matrices[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                                if is_hall_generated == False:
                                    is_hall_generated = True
                                historique.append(self.matrices[iy].copy())
                                break
        return Donjon
    
    def generate_json(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        shape = self.matrices.shape
        
        # On retire tout les chemins qui superpose des salles
        blacklist_chemin = []
        clean_list_dead_end = []     
        for etage in self.salle_generer:
            for pos_2d in etage:
                room = etage[pos_2d]
                room_shape = room.matrice.shape
                for posy in range(room_shape[0]):
                    for posx in range(room_shape[1]):
                        for posz in range(room_shape[2]):
                            if self.matrices[room.position[0]+posy,room.position[1]+posx,room.position[2]+posz] == 3 and room.matrice[posy,posx,posz] != 0:
                                blacklist_chemin.append((room.position[0]+posy,room.position[1]+posx,room.position[2]+posz))
                            if room.matrice[posy,posx,posz] ==  5:
                                for i,direction in enumerate(directions):
                                    cord_voisin = (room.position[0]+posy,room.position[1]+posx+direction[0],room.position[2]+posz+direction[1])
                                    if 0<=cord_voisin[1]<shape[1] and 0<=cord_voisin[2]<shape[2]:
                                        if self.matrices[cord_voisin] == 0 :
                                            cord_voisin = (cord_voisin[0]*7,(shape[1]-cord_voisin[1])*7,cord_voisin[2]*7)
                                            clean_list_dead_end.append({"filename":"dead_end","position":cord_voisin,"rotation":0,"origin":(posy,posx,posz)})


                                    
        clean_list_salle = []
        for etage in self.salle_generer:
            for pos_2d in etage:
                salle = etage[pos_2d]
                salle.position = [salle.position[0]*7,(shape[1]-salle.position[1])*7,salle.position[2]*7]
                salle.position = [salle.position[0]+salle.position_structure_block[0],salle.position[1]+salle.position_structure_block[1],salle.position[2]+salle.position_structure_block[2]]
                clean_list_salle.append({"filename":salle.RoomType.filename,"position":salle.position,"rotation":salle.rotation,"mirror":salle.miror})

        clean_list_chemin = []
        # axe X et axe Z
        # (-1,0) -1 sur l'axe X, (1,0) 1 sur l'axe X
        # (0,-1) -1 sur l'axe Z, (0,1) 1 sur l'axe Z "0110","1111","0111","1100"
        Chemin_L = ["0110","1010","1001","0101"]
        Chemin_X = ["1111"]
        Chemin_T = ["0111","1110","1011","1101"]
        Chemin_I = ["1100","0011"]
        possibilite = [Chemin_L,Chemin_X,Chemin_T,Chemin_I]
        for posy in range(shape[0]):
            for posx in range(shape[1]):
                for posz in range(shape[2]):
                    if self.matrices[(posy,posx,posz)] == 3:
                        chemin_code = ""
                        for i,direction in enumerate(directions):
                            cord_voisin = (posy,posx+direction[0],posz+direction[1])
                            if 0<=cord_voisin[1]<shape[1] and 0<=cord_voisin[2]<shape[2]:
                                if self.matrices[cord_voisin] == 3 :
                                    chemin_code+= "1"
                                else:
                                    chemin_code+= "0"
                            else:
                                chemin_code+= "0"
                        for chemin_type in possibilite:
                            for index,type in enumerate(chemin_type):
                                if chemin_code == type:
                                    #correction de la position

                                    if (posy,posx,posz) not in blacklist_chemin:
                                        position = [posy*7,(shape[1]-posx)*7,posz*7]
                                        if index == 1:
                                            position[1] += 6
                                            clean_list_chemin.append({"filename":random.choice(self.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                        elif index == 2:
                                            position[1] += 6
                                            position[2] += 6
                                            clean_list_chemin.append({"filename":random.choice(self.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                        elif index == 3:
                                            position[2] += 6
                                            clean_list_chemin.append({"filename":random.choice(self.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                        else:
                                            clean_list_chemin.append({"filename":random.choice(self.Room_Type[chemin_type[0]]),"position":position,"rotation":0,"mirror":False})
                                        # ajout a la lite
        
        self.json_data = json.dumps(clean_list_salle + clean_list_chemin + clean_list_dead_end)
        return self.json_data