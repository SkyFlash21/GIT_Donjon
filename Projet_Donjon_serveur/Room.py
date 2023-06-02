import numpy as np

class Room:
    def __init__(self, RoomType,rotation,miror):
        self.RoomType = RoomType 
        self.position = (0,0,0)
        self.rotation = rotation
        self.miror = miror
        self.matrice_originale = RoomType.matrice
        self.matrice = RoomType.matrice
        
    def GetRoom(self):
        return {"name":self.RoomType.name,"filename":self.RoomType.filename,"position":self.position,"local_position":(self.position[1],self.position[2]),"rotation":self.rotation,"mirror":self.miror,"matrice":self.matrice,"connected_room":[],"connecteur":np.argwhere(self.matrice == 5).tolist()}
