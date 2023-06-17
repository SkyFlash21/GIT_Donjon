from Donjon import *
from RoomType import *
from Generate import *
import numpy as np
from Util import *
import os
import sys

def loadRequierement():
    reqFile = "requirement.txt"
    with open(reqFile, "r", encoding="utf-8") as f:
        reqInstall = f.readlines()
    makeInstall = []
    for i in reqInstall:
         if str(i) not in sys.modules:
              makeInstall.append(i)

    if len(makeInstall) != 0: 
        for i in range(len(makeInstall)):
            command = str('py -m pip' + " " + "" 'install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org --user' + " " + str(makeInstall[i]).replace("\n", ""))
            os.system(command)
while True:
    Valide = True
    val = []
    Instance = Donjon(Taille_Matrice=(2,20,20),Nombre_de_Salle=(10,20))

    # Ajout des salles au donjon
    Instance.Room_Type["hall"].append(RoomType("debug_hall_1", "Salle de test",np.array([[[1,5,1], [5,1,5], [1,5,1]]]),filename = None))
    Instance.Room_Type["2_etage"].append(RoomType("debug_escalier_2", "Salle de test",np.array([[[1,0], [1,1], [1,5], [1,1]],[[1,0], [5,1], [1,1], [1,1]]]),filename = None))
    Instance.Room_Type["1_etage"].append(RoomType("debug_room_1", "Salle de test",np.array([[[1,1], [1,5], [1,1]]]),filename = None))
    Instance.Room_Type["1_etage"].append(RoomType("debug_room_3", "Salle de test",np.array([[[1,5,1], [1,1,5], [0,1,1]]]),filename = None))
    Instance = Generate(Instance,1)

    for etage in range(len(Instance.matrices)):
        # On trouve l'origine de l'étage (salle qui fait escalier entre deux étage)
        origin_etage = None
        if etage != 0:
            for room in Instance.salle_generer[etage-1].values():
                if len(room.matrice) == 2:
                    origin_etage = room
        elif etage == 0:
            for room in Instance.salle_generer[etage].values():
                if "hall" in room.RoomType.name:
                    origin_etage = room

        ordered = Instance.Get_Distance_from_center(origin_etage,etage) # Tri des salles en foncion de la distance

        tentative_discconnected = 0
        disconnected = Instance.Get_disconnected_room(etage)
        while disconnected != []:
            tentative_discconnected += 1
            if tentative_discconnected > 100:
                break
            if len(disconnected) == 1:
                if "hall" in disconnected[0].RoomType.name:
                    break
            for roomA in ordered:
                if roomA in disconnected :
                    print(f"{roomA.position} est déconecté")
                    nearest_connected_room = Instance.Get_nearest_connected_room(roomA)
                    if nearest_connected_room == None:
                        break
                    print(f"tentative de connection entre {roomA.position} {nearest_connected_room.position}",len(ordered))
                    
                    Aindex,Bindex,connector = Instance.Connect_rooms(roomA,nearest_connected_room)

                    if connector != None:
                        print("Connector Found")
                        path_betwen_point = PathFinding.find_shortest_path(Instance.matrices,connector[0],connector[1],{3:1,0:3})
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
                                Instance.matrices[point] = 3
                        else:
                            roomA.failed.append(nearest_connected_room)
                            nearest_connected_room.failed.append(roomA)
                    else:
                        roomA.failed.append(nearest_connected_room)
                        nearest_connected_room.failed.append(roomA)
            disconnected = Instance.Get_disconnected_room(etage)
            

    del Instance
