import numpy as np
import math

class Room:
    def __init__(self, RoomType,rotation,miror):
        self.RoomType = RoomType 
        self.position = (0,0,0)
        self.rotation = rotation
        self.miror = miror
        self.matrice_originale = RoomType.matrice
        self.matrice = RoomType.matrice
        self.connecteur_global = [[],[]]

        self.salle_connecter = []
        self.failed = []
    
    def Update_connecteur_global(self):
        connecteur_local = [np.argwhere(self.matrice == 5).tolist(),[]]
        for connecteur in connecteur_local[0]:
            pos = [0,connecteur[0],connecteur[1]]
            for i in range(len(connecteur)):
                pos[i] = connecteur[i] + self.position[i]
            
            self.connecteur_global[0].append((pos[0],pos[1],pos[2]))


    def GetRoom(self):
        return {"name":self.RoomType.name,"filename":self.RoomType.filename,"position":self.position,"local_position":(self.position[1],self.position[2]),"rotation":self.rotation,"mirror":self.miror,"matrice":self.matrice}
    
    def Get_nearest_connected_room(self,list):
        list = list.copy()
        ordered_list = []
        for room in list.value():
            print(room.position)

