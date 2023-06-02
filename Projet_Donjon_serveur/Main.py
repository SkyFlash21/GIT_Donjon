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

Instance = Donjon(Taille_Matrice=(20,20,20),Nombre_de_Salle=(60,100))

# Ajout des salles au donjon
Instance.Room_Type[1].append(RoomType("wood_5", "Salle de test",(1,1,2),np.array([[[1, 5, 1], [0, 1, 1], [0, 1, 1], [0, 1, 1]],[[0, 0, 0], [0, 1, 1], [5, 1, 1], [0, 1, 1]]]),filename = None))
Instance.Room_Type[0].append(RoomType("wood_2", "Salle de test",(1,1,2),np.array([[[5, 0, 5], [1, 1, 1], [0, 1, 0]]]),filename = None))
Instance = Generate(Instance,1)
print(clean_list(Instance))
del Instance