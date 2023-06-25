import numpy as np
import math
import Util

class Room:
    def __init__(self, RoomType,rotation,miror):
        self.RoomType = RoomType 
        self.position = (0,0,0)
        self.rotation = rotation
        self.miror = False
        self.matrice_originale = RoomType.matrice
        self.matrice = RoomType.matrice
        self.connecteur_global = [[],[]]
        self.position_structure_block = (0,0,0)

        self.salle_connecter = []
        self.failed = []
    
    def Update_connecteur_global(self):
        connecteur_local = [np.argwhere(self.matrice == 5).tolist(),[]]
        for connecteur in connecteur_local[0]:
            pos = [0,connecteur[0],connecteur[1]]
            for i in range(len(connecteur)):
                pos[i] = connecteur[i] + self.position[i]
            self.connecteur_global[0].append((pos[0],pos[1],pos[2]))

    def Rotate_Room(self, angle=None):
        print(self.rotation)
        original_shape = self.matrice_originale.shape
        matrice = self.matrice_originale
        if "hall" == self.RoomType.name[-4:]:
            self.position_structure_block = [0,-14,0]
            return
        
        # valide
        if angle == 0:
            self.position_structure_block = [0,(-original_shape[1]*7)+7,0]
            self.matrice = matrice
            self.rotation = 0

        elif angle == 1:
            nouvelle_matrice = np.rot90(matrice, k=3, axes=(1, 2))
            self.position_structure_block = [0,6,0]
            self.matrice = nouvelle_matrice
            self.rotation = 1

        elif angle == 2:
            nouvelle_matrice = np.rot90(matrice, k=2, axes=(1, 2))
            self.matrice = nouvelle_matrice
            self.position_structure_block = [0,+6,original_shape[2]*7-1]
            self.rotation = 2
        
        elif angle == 3:
            nouvelle_matrice = np.rot90(matrice, axes=(1, 2))
            self.matrice = nouvelle_matrice
            self.position_structure_block = [0,(-original_shape[2]*7)+7,original_shape[1]*7-1]
            self.rotation = 3
        

    def GetRoom(self):
        return {"name":self.RoomType.name,"filename":self.RoomType.filename,"position":self.position,"local_position":(self.position[1],self.position[2]),"rotation":self.rotation,"mirror":self.miror,"matrice":self.matrice}
    
    def Get_nearest_connected_room(self,list):
        list = list.copy()
        ordered_list = []
        for room in list.value():
            print(room.position)

