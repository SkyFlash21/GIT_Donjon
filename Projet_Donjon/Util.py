import matplotlib.pyplot as plt
import os

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

def clean_salle_list(Donjon):
    clean_list_salle = []
    for etage in Donjon.salle_generer:
        for pos_2d in etage:
            salle = etage[pos_2d]
            clean_list_salle.append({salle["filename"],salle["rotation"],salle["mirror"]})

    clean_list_chemin = []
    shape = Donjon.matrices.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    correspondance_code = ["1100","1110","1010","1111"]
    possibilite = []
    for posy in range(shape[0]):
        for posx in range(shape[1]):
            for posz in range(shape[2]):
                if Donjon.matrices[(posy,posx,posz)] == 3:
                    chemin_code = ""
                    debug = []
                    for i,direction in enumerate(directions):
                        cord_voisin = (posy,posx+direction[0],posz+direction[1])
                        if 0<=cord_voisin[1]<shape[1] and 0<=cord_voisin[2]<shape[2]:
                            debug.append((Donjon.matrices[cord_voisin],cord_voisin))
                            if Donjon.matrices[cord_voisin] == 3 or Donjon.matrices[cord_voisin] == 5 :
                                chemin_code+= "1"
                            else:
                                chemin_code+= "0"
                        else:
                            chemin_code+= "0"
                    if chemin_code == "0000":
                        print(debug)
                    if not chemin_code in possibilite:
                        possibilite.append(chemin_code)
    print(possibilite)
    return (clean_list_salle + clean_list_chemin)
