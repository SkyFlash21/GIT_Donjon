from Donjon import *
from RoomType import *
from Generate import *
import numpy as np

Instance = Donjon(Taille_Matrice=(20,20,20),Nombre_de_Salle=(60,100))

# Ajout des salles au donjon
Instance.Room_Type[1].append(RoomType("wood_5", "Salle de test",(1,1,2),np.array([[[1, 5, 1], [0, 1, 1], [0, 1, 1]],[[0, 0, 0], [0, 1, 1], [0, 1, 1]]]),filename = None))
Instance.Room_Type[0].append(RoomType("wood_2", "Salle de test",(1,1,2),np.array([[[5, 0, 5], [1, 1, 1], [0, 1, 0]]]),filename = None))

Generate(Instance,1)