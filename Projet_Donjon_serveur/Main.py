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

import time

start_time = time.time()
def Generate_dungeon(size,nombre_salle,theme):
    Donjon_valide = False
    while Donjon_valide == False: 
        Instance = Donjon(Taille_Matrice=(size),Nombre_de_Salle=nombre_salle)

        # Ajout des salles au donjon
        if theme == "debug":
            Instance.Room_Type[0].append(RoomType("debug_hall", "Salle de test",np.array([[[1,5,1], [5,3,5], [1,5,1]]]),"hall"))
            Instance.Room_Type[2].append(RoomType("debug_escalier_2", "Salle de test",np.array([[[1,0], [1,1], [1,5], [1,1]],[[1,0], [5,1], [1,1], [1,1]]]),"escalier"))
            Instance.Room_Type[1].append(RoomType("debug_room_1", "Salle de test",np.array([[[1,1], [1,5], [1,1]]])))
            Instance.Room_Type[1].append(RoomType("debug_room_3", "Salle de test",np.array([[[1,5,1], [1,3,5], [0,1,1]]])))
            Instance.Room_Type["0110"] = ["0110"]
            Instance.Room_Type["1111"] = ["1111"]
            Instance.Room_Type["0111"] = ["0111"]
            Instance.Room_Type["1100"] = ["1100"]
        elif theme == "mine":
            Instance.Room_Type[0].append(RoomType("mine_hall", "Salle de test",np.array([[[1,5,1], [5,3,5], [1,5,1]],[[1,1,1], [1,1,1], [1,1,1]]])))
            Instance.Room_Type[2].append(RoomType("debug_escalier_2", "Salle de test",np.array([[[1,0], [1,1], [1,5], [1,1]],[[1,0], [5,1], [1,1], [1,1]]])))
            Instance.Room_Type[1].append(RoomType("mine_altar", "Salle de test",np.array([[[1,1,1], [1,1,1], [1,5,1]]])))
            Instance.Room_Type[1].append(RoomType("mine_flora", "Salle de test",np.array([[[1,1,1], [1,1,1], [1,5,1]]])))
            Instance.Room_Type["1100"] = ["1100_1_mine","1100_2_mine","1100_3_mine","1100_4_mine","1100_5_mine","1100_6_mine","1100_7_mine","1100_8_mine","1100_9_mine","1100_10_mine"]
            Instance.Room_Type["0110"] = ["0110_1_mine","0110_2_mine","0110_3_mine","0110_4_mine"]
            Instance.Room_Type["1111"] = ["1111_1_mine","1111_2_mine"]
            Instance.Room_Type["0111"] = ["0111"]

        Instance.Generate()
        Donjon_valide = Instance.is_dungeon_valid()

        
        if Donjon_valide:
            json = Instance.generate_json()
            print(json)
            return (Instance,"--- %s seconds ---" % (time.time() - start_time))
        else:
            del Instance

