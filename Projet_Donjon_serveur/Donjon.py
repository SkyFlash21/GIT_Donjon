import numpy as np

class Donjon:
    def __init__(self,Taille_Matrice,Nombre_de_Salle):
        self.matrices = np.zeros((Taille_Matrice[0], Taille_Matrice[1], Taille_Matrice[2])).astype(int) # Matrice du donjon, c'est ici que les salles vérifieront si elle peuvent se placer sans superposer une autre salle.
        self.taille = Taille_Matrice # Taille du donjon 
        self.Room_Type = [[],[],[]] # Type de salle (preset) classé par étage, une salle qui s'étend sur un étage auras l'index 0, deux étage : l'index 1 et trois étage l'index 2

        self.salle_generer = [] # Liste 
        self.json_data = None # Data envoyé au serveur [non fini]
        self.Nombre_de_Salle = Nombre_de_Salle # Nombre de salle voulu pour le donjon au minimum et au maximum (tuple)
