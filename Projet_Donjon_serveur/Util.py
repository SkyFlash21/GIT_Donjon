import matplotlib.pyplot as plt
import json
import numpy as np
import math,random

def afficher_matrice(matrice):
    # Créer une figure et un axe
    fig, ax = plt.subplots()

    # Créer une carte de couleurs
    cmap = plt.get_cmap('viridis')

    # Afficher la matrice comme une image avec une couleur par valeur
    img = ax.imshow(matrice, cmap=cmap)

    # Ajouter une barre de couleurs à côté de la grille
    cbar = plt.colorbar(img)

    # Afficher la grille sans les graduations
    ax.grid(False)

    # Afficher la figure
    plt.show()

def convert_to_tuples(paths):
    converted_paths = []
    for path in paths:
        converted_path = []
        for point in path:
            converted_path.append(tuple(point.tolist()))
        converted_paths.append(tuple(converted_path))
    return converted_paths

def generate_coordinate_codes(matrix,cord):
    codes = {}
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 3:
                continue

            adjacent_count = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue  # Skip the current coordinate
                    x = i + dx
                    y = j + dy
                    if 0 <= x < rows and 0 <= y < cols and matrix[x][y] == 3:
                        adjacent_count += 1

            code = format(adjacent_count, '04b')  # Convert the count to binary with 4 digits
            codes[(i, j)] = code

    return codes

def clean_list(Donjon):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    shape = Donjon.matrices.shape
    
    # On retire tout les chemins qui superpose des salles
    blacklist_chemin = []
    clean_list_dead_end = []     
    for etage in Donjon.salle_generer:
        for pos_2d in etage:
            room = etage[pos_2d]
            room_shape = room.matrice.shape
            for posy in range(room_shape[0]):
                for posx in range(room_shape[1]):
                    for posz in range(room_shape[2]):
                        if Donjon.matrices[room.position[0]+posy,room.position[1]+posx,room.position[2]+posz] == 3 and room.matrice[posy,posx,posz] != 0:
                            blacklist_chemin.append((room.position[0]+posy,room.position[1]+posx,room.position[2]+posz))
                        if room.matrice[posy,posx,posz] ==  5:
                            for i,direction in enumerate(directions):
                                cord_voisin = (room.position[0]+posy,room.position[1]+posx+direction[0],room.position[2]+posz+direction[1])
                                if 0<=cord_voisin[1]<shape[1] and 0<=cord_voisin[2]<shape[2]:
                                    if Donjon.matrices[cord_voisin] == 0 :
                                        cord_voisin = (cord_voisin[0]*7,(shape[1]-cord_voisin[1])*7,cord_voisin[2]*7)
                                        clean_list_dead_end.append({"filename":"dead_end","position":cord_voisin,"rotation":0,"origin":(posy,posx,posz)})


                                 
    clean_list_salle = []
    for etage in Donjon.salle_generer:
        for pos_2d in etage:
            salle = etage[pos_2d]
            salle.position = [salle.position[0]*7,(shape[1]-salle.position[1])*7,salle.position[2]*7]
            salle.position = [salle.position[0]+salle.position_structure_block[0],salle.position[1]+salle.position_structure_block[1],salle.position[2]+salle.position_structure_block[2]]
            clean_list_salle.append({"filename":salle.RoomType.filename,"position":salle.position,"rotation":salle.rotation,"mirror":salle.miror})

    clean_list_chemin = []
    # axe X et axe Z
    # (-1,0) -1 sur l'axe X, (1,0) 1 sur l'axe X
    # (0,-1) -1 sur l'axe Z, (0,1) 1 sur l'axe Z
    Chemin_L = ["0110","1010","1001","0101"]
    Chemin_X = ["1111"]
    Chemin_T = ["0111","1110","1011","1101"]
    Chemin_I = ["1100","0011"]
    possibilite = [Chemin_L,Chemin_X,Chemin_T,Chemin_I]
    for posy in range(shape[0]):
        for posx in range(shape[1]):
            for posz in range(shape[2]):
                if Donjon.matrices[(posy,posx,posz)] == 3:
                    chemin_code = ""
                    for i,direction in enumerate(directions):
                        cord_voisin = (posy,posx+direction[0],posz+direction[1])
                        if 0<=cord_voisin[1]<shape[1] and 0<=cord_voisin[2]<shape[2]:
                            if Donjon.matrices[cord_voisin] == 3 :
                                chemin_code+= "1"
                            else:
                                chemin_code+= "0"
                        else:
                            chemin_code+= "0"
                    for chemin_type in possibilite:
                        for index,type in enumerate(chemin_type):
                            if chemin_code == type:
                                #correction de la position

                                if (posy,posx,posz) not in blacklist_chemin:
                                    position = [posy*7,(shape[1]-posx)*7,posz*7]
                                    if index == 1:
                                        position[1] += 6
                                        clean_list_chemin.append({"filename":random.choice(Donjon.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                    elif index == 2:
                                        position[1] += 6
                                        position[2] += 6
                                        clean_list_chemin.append({"filename":random.choice(Donjon.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                    elif index == 3:
                                        position[2] += 6
                                        clean_list_chemin.append({"filename":random.choice(Donjon.Room_Type[chemin_type[0]]),"position":position,"rotation":index,"mirror":False})
                                    else:
                                        clean_list_chemin.append({"filename":random.choice(Donjon.Room_Type[chemin_type[0]]),"position":position,"rotation":0,"mirror":False})
                                    # ajout a la lite
    
    return json.dumps(clean_list_salle + clean_list_chemin + clean_list_dead_end)

def Compare_tuple(Atuple,Btuple):
    compare = True
    for i in range(3):
        if Atuple[i] != Btuple[i]:
            compare = False
    return compare

def rotation_matrice(matrice):
    lignes = len(matrice)
    colonnes = len(matrice[0])

    # Créer un nouvel array vide avec les dimensions inversées
    matrice_rot = np.zeros((colonnes, lignes), dtype=int)

    # Parcourir la matrice d'origine et remplir le nouvel array tourné
    for i in range(lignes):
        for j in range(colonnes):
            matrice_rot[j][lignes - i - 1] = matrice[i][j]

    return matrice_rot