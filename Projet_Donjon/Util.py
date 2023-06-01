import matplotlib.pyplot as plt

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