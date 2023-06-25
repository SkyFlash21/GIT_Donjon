import numpy as np

def pivoter_matrice_3d(matrice, angle):
    matrice_np = np.array(matrice)
    
    if angle == 0:
        return matrice_np
    
    elif angle == 90:
        nouvelle_matrice = np.rot90(matrice_np, axes=(1, 2))
        return nouvelle_matrice
    
    elif angle == 180:
        nouvelle_matrice = np.rot90(matrice_np, k=2, axes=(1, 2))
        return nouvelle_matrice
    
    elif angle == 270:
        nouvelle_matrice = np.rot90(matrice_np, k=3, axes=(1, 2))
        return nouvelle_matrice

# Exemple d'utilisation
matrice_3d = [[[1, 0], [1, 1], [1, 5], [1, 1]],
              [[1, 1], [1, 5], [1, 1], [1, 0]]]

angle_rotation = 90
nouvelle_matrice_3d = pivoter_matrice_3d(matrice_3d, angle_rotation)
print(nouvelle_matrice_3d)
