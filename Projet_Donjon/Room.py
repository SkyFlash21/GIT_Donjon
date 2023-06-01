import numpy as np

class Room:
    def __init__(self, RoomType,rotation,miror):
        self.RoomType = RoomType 
        self.position = (0,0,0)
        self.rotation = rotation
        self.miror = miror
        self.matrice_originale = RoomType.matrice
        self.matrice = RoomType.matrice
        if rotation != 0 :
            self.matrice = np.rot90(self.matrice, axes=(1, 2))
        if miror == True :
            self.matrice = np.flip(self.matrice, axis=1)
        
    def GetRoom(self):
        return {"name":self.RoomType.name,"filename":self.RoomType.filename,"position":self.position,"local_position":(self.position[1],self.position[2]),"rotation":self.rotation,"mirror":self.miror,"matrice":self.matrice,"connected_room":[],"connecteur":np.argwhere(self.matrice == 5).tolist()}
