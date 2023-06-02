import matplotlib.pyplot as plt
import json
import numpy as np

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

def clean_list(Donjon):
    clean_list_salle = []
    for etage in Donjon.salle_generer:
        for pos_2d in etage:
            salle = etage[pos_2d]
            clean_list_salle.append({"filename":salle["filename"],"position":salle["position"],"rotation":salle["rotation"],"mirror":salle["mirror"]})

    clean_list_chemin = []
    shape = Donjon.matrices.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    Chemin_L = ["1010","1001","0101","0110"]
    Chemin_X = ["1111"]
    Chemin_T = ["1011","1110","0111","1101"]
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
                            if Donjon.matrices[cord_voisin] == 3 or Donjon.matrices[cord_voisin] == 5 or Donjon.matrices[cord_voisin] == 4:
                                chemin_code+= "1"
                            else:
                                chemin_code+= "0"
                        else:
                            chemin_code+= "0"
                    for chemin_type in possibilite:
                        if chemin_code in chemin_type:
                            clean_list_chemin.append({"filename":chemin_code,"position":[posy,posx,posz],"rotation":chemin_type.index(chemin_code),"mirror":False})
    return json.dumps(clean_list_salle + clean_list_chemin)

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