
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

            if is_hall_generated == False:
                selected_room = random.choice(Donjon.Room_Type["hall"]).GenerateRoom()
            else:
                if stage_escalier > 0 and iy != len(Donjon.matrices)-1:
                    selected_room = random.choice(Donjon.Room_Type["2_etage"]).GenerateRoom()
                    stage_escalier-=1
                else:
                    selected_room = random.choice(Donjon.Room_Type["1_etage"]).GenerateRoom()

            selected_room_shape = selected_room.matrice.shape
            
            # Définition de la rotation de la salle
            if selected_room.rotation != 0:
                # Pour chaque étage de la salle
                matrices_etage = []
                for i,stage in enumerate(selected_room.matrice_originale):
                    matrice_rotated = selected_room.matrice_originale[i]
                    for j in range(0,selected_room.rotation):
                        matrice_rotated = Util.rotation_matrice(matrice_rotated)
                    matrices_etage.append(matrice_rotated)

                rotated_shape = matrices_etage[0].shape
                selected_room.matrice = np.zeros((selected_room_shape[0],rotated_shape[0],rotated_shape[1]), dtype=int)
                for i,etage in enumerate(matrices_etage):
                    selected_room.matrice[i] = matrices_etage[i]

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

                debug_connector = []
                for posy in range(rotated_shape[0]):
                    if valide == False : break
                    for posx in range(rotated_shape[1]):
                        if valide == False : break
                        for posz in range(rotated_shape[2]):
                            if valide == False : break
                            # Test de superposition
                            if Donjon.matrices[(position[0]+posy,position[1]+posx,position[2]+posz)] + selected_room.matrice[posy,posx,posz] in [0,1,5]:
                                pass
                            else:
                                # non valide
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
                    
                    matrice_copy = Donjon.matrices.copy()
                    matrice_copy[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                    connecteur_libre = False
                    for posy in range(rotated_shape[0]):
                        for posx in range(rotated_shape[1]):
                            for posz in range(rotated_shape[2]):

                                connecteur_libre = False
                                for dir in direction:
                                    if  0 < position[1]+posx+dir[0] < global_shape[1]-1 and 0 < position[2]+posz+dir[1] < global_shape[2]-1 :
                                        if matrice_copy[posy,position[1]+posx+dir[0],position[2]+posz+dir[1]] == 0:
                                            connecteur_libre = True
                                        matrice_copy[posy,position[1]+posx+dir[0],position[2]+posz+dir[1]] = 6

                    if 5 not in Donjon.matrices[position[0]:position[0]+rotated_shape[0],max(0,position[1]-1):min(global_shape[1],position[1]+rotated_shape[1]+2),max(0,position[2]-1):min(global_shape[2],position[2]+rotated_shape[2]+2)] and connecteur_libre:
                        selected_room.position = position
                        selected_room.Update_connecteur_global()
                        Donjon.salle_generer[iy][selected_room.position] = selected_room
                        Donjon.matrices[position[0]:position[0]+rotated_shape[0],position[1]:position[1]+rotated_shape[1],position[2]:position[2]+rotated_shape[2]] = selected_room.matrice
                        if is_hall_generated == False:
                            is_hall_generated = True
                        print(position,debug_connector)
                        historique.append(Donjon.matrices[iy].copy())
                        break
        print("Affichage de l'étage",iy)
        Util.afficher_matrice(Donjon.matrices[iy])
        direction = [(1,0),(-1,0),(0,1),(0,-1)]
        user_input = "None"
        while user_input != "":
            user_input = input("next or debug\n")
            if user_input == "debug":
                global_shape = Donjon.matrices.shape
                for posy in range(global_shape[0]):
                    for posx in range(global_shape[1]):
                        for posz in range(global_shape[2]):
                            if Donjon.matrices[posy,posx,posz] == 5:
                                connecteur_libre = False
                                valeur = []
                                for dir in direction:
                                    if  0 < posx+dir[0] < global_shape[1]-1 and 0 < posz+dir[1] < global_shape[2]-1 :
                                        if matrice_copy[posy,posx+dir[0],posz+dir[1]] == 0:
                                            connecteur_libre = True
                                        valeur.append(matrice_copy[posy,posx+dir[0],posz+dir[1]] )
                                if connecteur_libre == False:
                                    print("False",(posy,posx,posz),valeur)
            elif user_input == "show":
                Util.afficher_matrice(Donjon.matrices[iy])
            elif user_input == "historique":
                for stage in historique:
                    Util.afficher_matrice(stage)



    return Donjon