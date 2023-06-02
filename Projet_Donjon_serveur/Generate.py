
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
    for iy,y in enumerate(Donjon.matrices):
        Donjon.salle_generer.append({})
        stage_escalier = nbr_escalier

        # Placement des salles dans la matrices
        nombre_de_salle = random.randint(Donjon.Nombre_de_Salle[0],Donjon.Nombre_de_Salle[1])
        for i in range(nombre_de_salle):

            if stage_escalier > 0 and iy != len(Donjon.matrices)-1:
                selected_room = random.choice(Donjon.Room_Type[1]).GenerateRoom()
                stage_escalier-=1
            else:
                selected_room = random.choice(Donjon.Room_Type[0]).GenerateRoom()
            validation = True

            for tentative in range(50):
                # Définition aléatoire de la position dans l'étage
                shape = selected_room.matrice.shape
                x,z = random.randint(0,len(Donjon.matrices[1])-shape[1]),random.randint(0,len(Donjon.matrices[1])-shape[2])
                
                # Définition de la position de la salle
                selected_room.position = (iy,x,z)

                # Définition de la rotation de la salle
                for j in range(0,selected_room.rotation):
                    for i,stage in enumerate(selected_room.matrice):
                        print(selected_room.matrice[i])
                        selected_room.matrice[i] = np.rot90(selected_room.matrice[i], k=1, axes=(1, 0))
                        print(selected_room.matrice[i])
                        input(selected_room.RoomType.name)
                
                # Définition du fait que la salle soit en miroir ou non
                if selected_room.miror:
                    for i,stage in enumerate(selected_room.matrice):
                        selected_room.matrice[i] = np.flip(selected_room.matrice[i], axis=1)

                # On vérifie que la salle peux être posé 
                for posy in range(shape[0]):
                    for posx in range(shape[1]):
                        for posz in range(shape[2]):
                            if Donjon.matrices[iy+posy,x+posx,z+posz]+selected_room.matrice[posy,posx,posz] not in [0,1,5]:
                                validation = False
                                
                if validation:
                    room = selected_room.GetRoom()
                    Donjon.salle_generer[iy][room["local_position"]] = room
                    for posy in range(shape[0]):
                        for posx in range(shape[1]):
                            for posz in range(shape[2]):
                                if selected_room.matrice[posy,posx,posz] != 0:
                                    Donjon.matrices[iy+posy,x+posx,z+posz] = selected_room.matrice[posy,posx,posz]
                    break

        # Une fois arrivé à se point, cela veux dire que les salles on été genéré
        # Ici on génère les différentes connection entre les salles tout est en 2d (pour chaque étage)
        # La matrice est recrée afin d'avoir une valeur par salle, se qui permet de faire un calcul des chemins entre les salles (Deulanay)
        shape = Donjon.matrices.shape
        Matrice_salle = np.zeros((shape[1],shape[2])) # Géneration d'une matrice 2d
        Matrice_connection = {}

        # Initialisation des valeurs dans la matrice, on mets en place les salles ainsi que leurs connecteurs
        salles_etage = Donjon.salle_generer[iy]

        # Pour chaque salle dans cette étage
        for point in list(salles_etage.values()):
            Matrice_salle[point["local_position"]] = 1 # On place la salle (coordonée de son orgine) dans la matrice
            result = [] # On crée une liste liste des connecteurs possible pour cette salle
            for i in point["connecteur"]:
                cord = (i[0] + point["position"][0],i[1] + point["position"][1],i[2] + point["position"][2])
                result.append(cord)

            Matrice_connection[point["local_position"]] = [result,[]] # On ajoute au dictionnaire Matrice_connection une liste avec les connecteurs disponible et ceux déja utilisé pour la salle 

        # Récupération des coordonnées des salles (origine)
        position_salles = np.argwhere(Matrice_salle == 1)

        # Triangulation de Delaunay
        tri = Delaunay(position_salles)

        edges = []

        # Parcourir chaque triangle
        for triangle in tri.simplices:
            # Générer toutes les arêtes possibles (combinaisons de deux points)
            # et les ajouter à la liste des arêtes
            edge1 = [position_salles[triangle[0]], position_salles[triangle[1]]]
            edge2 = [position_salles[triangle[1]], position_salles[triangle[2]]]
            edge3 = [position_salles[triangle[2]], position_salles[triangle[0]]]
            edges.extend([edge1, edge2, edge3])

        edges = Util.convert_to_tuples(edges)
        tree = Spanning_tree.minimum_spanning_tree(edges)
        random_tree = Spanning_tree.add_random_edges_to_minimum_spanning_tree(tree, edges, salles_etage)

        path_result = []
        # Ici on définie les coordonées de départ et de fin, on tente de connecter les salles entre elle en utilisant des connecteurs disponible, sinon on utilise des connecteurs déja utilisé
        for path in random_tree:
            local_path = []
            for cord in path:
                if len(Matrice_connection[cord][0]) == 0:
                    random_cord_1 = random.choice(Matrice_connection[cord][1])
                    local_path.append(random_cord_1)
                else:
                    random_cord_1 = random.choice(Matrice_connection[cord][0])
                    Matrice_connection[cord][1].append(random_cord_1)
                    Matrice_connection[cord][0].remove(random_cord_1)
                    local_path.append(random_cord_1)
            path_result.append(local_path)

        # Une fois les points de départ et d'arrivé définie on fait un pathfinding pour trouver les coordonées qui compose le chemin. Ensuite on place le chemin dans la matrice
        for path in path_result:
            all_route = PathFinding.find_shortest_path(Donjon.matrices[iy],(path[0][1],path[0][2]),(path[1][1],path[1][2]))
            if all_route != None:
                for block in all_route:
                    if Donjon.matrices[iy][block] == 0:
                        Donjon.matrices[iy][block] = 3
            else:
                Donjon.matrices[path[0]] = 4
                Donjon.matrices[path[1]] = 4
    print(PathFinding.find_disconnected_points(Donjon.matrices))
    return Donjon