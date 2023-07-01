from Room import *
import random

class RoomType:
    def __init__(self, name, description,matrice,type="salle"):
        self.name = name
        self.filename = name
        self.description = description
        self.type = type
        self.matrice = matrice # Matrice qui compose la salle, elle est soit de dimension 2 soit 3
        self.matrice_origin = matrice # Matrice originale
    
    def GenerateRoom(self):
        # On crée la nouvelle salles et on lui passe les arguments de positions et de type
        if "hall" == self.name[-4:]:
            room = Room(self)
        else:
            room = Room(self)
        return room