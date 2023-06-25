
"""
Pour chaque étage cette fonction place aléatoirement des salles, il place en priorité une salle qui permet de passer à l'étage suivant.
Par la suite il place le nombre de salle voulu dans l'étage.
Chaque salle est tourné ou mis en miroir aléatoirement pour avoir de la diversité
Chaque salle est testé jusqu'a quelle puisse être posé (max 50 essai)
Une fois que la salle est validé on la place dans la matrice et on l'ajoute à la liste salle_generer
"""

import random
import numpy as np
import PathFinding
import Util
from scipy.spatial import Delaunay
import Spanning_tree
import Outil_generation

def Generate(Donjon,nbr_escalier):
    is_hall_generated = False

    for iy,y in enumerate(Donjon.matrices):
        historique = []
        Donjon.salle_generer.append({})
        stage_escalier = nbr_escalier
        global_shape = Donjon.matrices.shape


        # Placement des salles dans la matrices
        nombre_de_salle = random.randint(Donjon.Nombre_de_Salle[0],Donjon.Nombre_de_Salle[1])
        for i in range(nombre_de_salle):

            # Géneration du hall ou des escaliers
            if is_hall_generated == False:
                selected_room = random.choice(Donjon.Room_Type["hall"]).GenerateRoom()
            else:
                if stage_escalier > 0 and iy != len(Donjon.matrices)-1:
                    selected_room = random.choice(Donjon.Room_Type["2_etage"]).GenerateRoom()
                    stage_escalier-=1
                else:
                    selected_room = random.choice(Donjon.Room_Type["1_etage"]).GenerateRoom()

            
            # Définition de la rotation de la salle
            
            selected_room.Rotate_Room(selected_room.rotation)
            if selected_room.RoomType.name[-4:] == "hall":
                selected_room.rotation = 0

            """ A REFAIRE
                # Définition du fait que la salle soit en miroir ou non
                if selected_room.miror:
                    for i,stage in enumerate(selected_room.matrice):
                        selected_room.matrice[i] = np.flip(selected_room.matrice[i], axis=1)
            """
            rotated_shape = selected_room.matrice.shape
            for tentative in range(50):
                direction = [(1,0),(-1,0),(0,1),(0,-1)]
                valide = True
                position = (iy,random.randint(0,global_shape[1]-rotated_shape[1]),random.randint(0,global_shape[2]-rotated_shape[2]))
                for posy in range(rotated_shape[0]):
                    if valide == False : break
                    for posx in range(rotated_shape[1]):
                        if valide == False : break
                        for posz in range(rotated_shape[2]):
                            if valide == False : break
                            # Test de superposition
                            if not Donjon.matrices[(position[0]+posy,position[1]+posx,position[2]+posz)] + selected_room.matrice[posy,posx,posz] in [0,1,3,5]:
                                valide = False

                            # Test d'accessibilité des connecteurs
                            if selected_room.matrice[posy,posx,posz] == 5:
                                # Exclusion des bordures
                                if posx+position[1] == global_shape[1]-1 or posx+position[1] == 0:
                                    valide = False
                                elif posz+position[2] == global_shape[2]-1 or posz+position[2] == 0:
                                    valide = False
                                    
                # Vérification que on bouche pas un connecteur

                if valide:
                    rotated_shape = selected_room.matrice.shape
                    matrice_copy = Donjon.matrices.copy()
                    matrice_copy[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                    if Outil_generation.verif_room_connector(matrice_copy):
                        if 5 not in Donjon.matrices[position[0]:position[0]+rotated_shape[0],max(0,position[1]-1):min(global_shape[1],position[1]+rotated_shape[1]+2),max(0,position[2]-1):min(global_shape[2],position[2]+rotated_shape[2]+2)]:
                            selected_room.position = position
                            selected_room.Update_connecteur_global()
                            Donjon.salle_generer[iy][selected_room.position] = selected_room
                            Donjon.matrices[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                            if is_hall_generated == False:
                                is_hall_generated = True
                            historique.append(Donjon.matrices[iy].copy())
                            break

    return Donjon