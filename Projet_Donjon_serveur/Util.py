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