from Room import *
import random

class RoomType:
    def __init__(self, name, description,matrice,filename = None):
        self.name = name
        self.filename = filename
        if filename == None: self.filename = name
        self.description = description
        self.matrice = matrice # Matrice qui compose la salle, elle est soit de dimension 2 soit 3
        self.matrice_origin = matrice # Matrice originale
    
    def GenerateRoom(self):
        # On crée la nouvelle salles et on lui passe les arguments de positions et de type
        if self.name == "debug_hall_1":
            room = Room(self,0,False)
        else:
            room = Room(self,random.randint(0,3),False)
        return room