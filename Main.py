import numpy as np
from scipy.spatial import Delaunay
import random
import heapq
import matplotlib.pyplot as plt

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX == rootY:
            return False
        if self.rank[rootX] < self.rank[rootY]:
            self.parent[rootX] = rootY
        elif self.rank[rootX] > self.rank[rootY]:
            self.parent[rootY] = rootX
        else:
            self.parent[rootY] = rootX
            self.rank[rootX] += 1
        return True

class Node:
    def __init__(self, row, col, g_cost=float('inf'), h_cost=0, parent=None):
        self.row = row
        self.col = col
        self.g_cost = g_cost  # Coût du chemin depuis le point de départ
        self.h_cost = h_cost  # Heuristique : estimation du coût jusqu'au point d'arrivée
        self.parent = parent  # Nœud parent dans le chemin

    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()

# Fonction de recherche du chemin le plus court
def find_shortest_path(matrix, start, end):
    rows = len(matrix)
    cols = len(matrix[0])

    # Vérifier si les points de départ et d'arrivée sont valides
    if not is_valid_point(start, rows, cols) or not is_valid_point(end, rows, cols):
        return None

    # Vérifier si les points de départ et d'arrivée sont vides
    if matrix[start[0]][start[1]] != 5 or matrix[end[0]][end[1]] != 5:
        return None

    # Définir les mouvements possibles (4 directions : haut, bas, gauche, droite)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialiser la liste ouverte et la liste fermée
    open_list = []
    closed_list = set()

    # Créer le nœud de départ et l'ajouter à la liste ouverte
    start_node = Node(start[0], start[1], g_cost=0, h_cost=calculate_heuristic(start, end))
    heapq.heappush(open_list, start_node)

    # Tant que la liste ouverte n'est pas vide
    while open_list:
        # Récupérer le nœud avec le coût total minimum de la liste ouverte
        current_node = heapq.heappop(open_list)

        # Vérifier si le nœud actuel est le nœud d'arrivée
        if current_node.row == end[0] and current_node.col == end[1]:
            # Reconstruire le chemin en remontant les nœuds parents
            path = []
            while current_node:
                path.append((current_node.row, current_node.col))
                current_node = current_node.parent
            return path[::-1]  # Inverser le chemin pour qu'il soit du point de départ au point d'arrivée

        # Ajouter le nœud actuel à la liste fermée
        closed_list.add((current_node.row, current_node.col))

        # Explorer les voisins du nœud actuel
        for direction in directions:
            next_row = current_node.row + direction[0]
            next_col = current_node.col + direction[1]

            # Vérifier si le voisin est dans les limites de la matrice
            if is_valid_point((next_row, next_col), rows, cols):
                # Vérifier si le voisin est un obstacle ou est déjà dans la liste fermée
                if matrix[next_row][next_col] == 1 or (next_row, next_col) in closed_list:
                    continue

                # Calculer le coût du chemin depuis le point de départ jusqu'au voisin
                g_cost = current_node.g_cost + 1

                # Vérifier si le voisin est déjà dans la liste ouverte
                is_in_open_list = False
                for node in open_list:
                    if node.row == next_row and node.col == next_col:
                        is_in_open_list = True
                        break

                # Si le voisin n'est pas dans la liste ouverte ou si le nouveau coût est plus faible
                if not is_in_open_list or g_cost < node.g_cost:
                    # Créer un nouveau nœud voisin
                    next_node = Node(next_row, next_col, g_cost=g_cost, h_cost=calculate_heuristic((next_row, next_col), end),
                                     parent=current_node)

                    # Ajouter le nœud voisin à la liste ouverte
                    heapq.heappush(open_list, next_node)

    # Aucun chemin trouvé
    return None

class Donjon:
    def __init__(self,Taille_Matrice,Nombre_de_Salle):
        self.matrices = np.zeros((Taille_Matrice[0], Taille_Matrice[1], Taille_Matrice[2])).astype(int) # Matrice du donjon, c'est ici que les salles vérifieront si elle peuvent se placer sans superposer une autre salle.
        self.taille = Taille_Matrice # Taille du donjon 
        self.Room_Type = [[],[],[]] # Type de salle (preset) classé par étage, une salle qui s'étend sur un étage auras l'index 0, deux étage : l'index 1 et trois étage l'index 2
    
        self.json_data = None # Data envoyé au serveur [non fini]
        self.Nombre_de_Salle = Nombre_de_Salle # Nombre de salle voulu pour le donjon au minimum et au maximum (tuple)

    """
        Pour chaque étage cette fonction place aléatoirement des salles, il place en priorité une salle qui permet de passer à l'étage suivant.
        Par la suite il place le nombre de salle voulu dans l'étage.
        Chaque salle est tourné ou mis en miroir aléatoirement pour avoir de la diversité
        Chaque salle est testé jusqu'a quelle puisse être posé (max 50 essai)
        Une fois que la salle est validé on la place dans la matrice et on l'ajoute à la liste salle_generer
    """
    def Generate(self,nbr_escalier):
        salle_generer = [] # Cette liste contient toutes les salles du donjon. Pour chaque étage il y a un dictionnaire avec mon index les positions des salles et valeur la salle en elle même.

        # Chaque étage
        for iy,y in enumerate(self.matrices):
            salle_generer.append({})
            stage_escalier = nbr_escalier

            # Placement des salles dans la matrices
            for i in range(random.randint(self.Nombre_de_Salle[0],self.Nombre_de_Salle[1])):
                # On fait 50 tentative de placement par salles
                # On sélectionne une salle aléatoirement dans la liste disponible des RoomTypes, on lui applique une rotation et un miror aléatoire avant de tenter de la parse.
                if stage_escalier > 0 and iy != len(self.matrices)-1:
                    selected_room = random.choice(self.Room_Type[1]).GenerateRoom()
                    stage_escalier-=1
                else:
                    selected_room = random.choice(self.Room_Type[0]).GenerateRoom()
                validation = True
                for tentative in range(50):
                    # Définition aléatoire de la position dans l'étage
                    shape = selected_room.matrice.shape
                    x,z = random.randint(0,len(self.matrices[1])-shape[1]),random.randint(0,len(self.matrices[1])-shape[2])
                    
                    selected_room.position = (iy,x,z)
                    for j in range(0,selected_room.rotation):
                        for i,stage in enumerate(selected_room.matrice):
                            selected_room.matrice[i] = np.rot90(selected_room.matrice[i], k=1, axes=(1, 0))
                    

                    if selected_room.miror:
                        for i,stage in enumerate(selected_room.matrice):
                            selected_room.matrice[i] = np.flip(selected_room.matrice[i], axis=1)

                    # On vérifie que la salle peux être posé 
                    for posy in range(shape[0]):
                        for posx in range(shape[1]):
                            for posz in range(shape[2]):
                                if self.matrices[iy+posy,x+posx,z+posz]+selected_room.matrice[posy,posx,posz] not in [0,1,5]:
                                    validation = False
                    A = self.matrices[iy]
                    if validation:
                        room = selected_room.GetRoom()
                        salle_generer[iy][room["local_position"]] = room
                        for posy in range(shape[0]):
                            for posx in range(shape[1]):
                                for posz in range(shape[2]):
                                    if selected_room.matrice[posy,posx,posz] != 0:
                                        self.matrices[iy+posy,x+posx,z+posz] = selected_room.matrice[posy,posx,posz]
                        break

            # Une fois arrivé à se point, cela veux dire que les salles on été genéré
            # Ici on génère les différentes connection entre les salles tout est en 2d (pour chaque étage)
            # La matrice est recrée afin d'avoir une valeur par salle, se qui permet de faire un calcul des chemins entre les salles (Deulanay)
            shape = self.matrices.shape
            Matrice_salle = np.zeros((shape[1],shape[2])) # Géneration d'une matrice 2d
            Matrice_connection = {}

            # Initialisation des valeurs dans la matrice, on mets en place les salles ainsi que leurs connecteurs
            points = salle_generer[iy]

            # Pour chaque salle dans cette étage
            for point in list(points.values()):
                Matrice_salle[point["local_position"]] = 1 # On place la salle (coordonée de son orgine) dans la matrice
                result = [] # On crée une liste liste des connecteurs possible pour cette salle
                for i in point["connecteur"]:
                    cord = (i[0] + point["position"][0],i[1] + point["position"][1],i[2] + point["position"][2])
                    result.append(cord)

                Matrice_connection[point["local_position"]] = [result,[]] # On ajoute au dictionnaire Matrice_connection une liste avec les connecteurs disponible et ceux déja utilisé pour la salle 
        
            result = get_point(Matrice_salle,points) # Recherche des chemins dans l'étage (cela retourne une liste contenant les chemins entre les salles, elle est sour la forme d'un point de départ et d'arrivé)

            path_result = []
            # Ici on définie les coordonées de départ et de fin, on tente de connecter les salles entre elle en utilisant des connecteurs disponible, sinon on utilise des connecteurs déja utilisé
            for path in result:
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
                all_route = find_shortest_path(self.matrices[iy],(path[0][1],path[0][2]),(path[1][1],path[1][2]))
                if all_route != None:
                    for block in all_route:
                        if self.matrices[iy][block] == 0:
                            self.matrices[iy][block] = 3
                else:
                    self.matrices[path[0]] = 4
                    self.matrices[path[1]] = 4
        print(find_disconnected_points(self.matrices))

    def afficher_etage(self,etage):
        for i,tree in enumerate(self.matrices[etage]):

            plt.figure()
            for u, v in tree:
                plt.plot([u[0], v[0]], [u[1], v[1]], 'b-')
            plt.scatter([point[0] for point in tree[0]], [point[1] for point in tree[0]], color='r', marker='o')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title(f'Graph {i} {len(tree)}')
            plt.grid(True)
        plt.show()

# Classe représentant un nœud dans la matrice


class RoomType:
    def __init__(self, name, description,taille,matrice,filename = None):
        self.name = name
        self.filename = filename
        if filename == None: self.filename = name
        self.description = description
        self.matrice = matrice # Matrice qui compose la salle, elle est soit de dimension 2 soit 3
    
    def GenerateRoom(self):
        # On crée la nouvelle salles et on lui passe les arguments de positions et de type
        room = Room(self,random.randint(0,4),random.choice([True,False]))
        return room
    
class Room:
    def __init__(self, RoomType,rotation,miror):
        self.RoomType = RoomType 
        self.position = (0,0,0)
        self.rotation = rotation
        self.miror = miror
        self.matrice_originale = RoomType.matrice
        self.matrice = RoomType.matrice
        if rotation != 0 :
            self.matrice = np.rot90(self.matrice, axes=(1, 2))
        if miror == True :
            self.matrice = np.flip(self.matrice, axis=1)
        
    
    def GetRoom(self):
        return {"name":self.RoomType.name,"filename":self.RoomType.filename,"position":self.position,"local_position":(self.position[1],self.position[2]),"rotation":self.rotation,"mirror":self.miror,"matrice":self.matrice,"connected_room":[],"connecteur":np.argwhere(self.matrice == 5).tolist()}

def convert_to_tuples(paths):
    converted_paths = []
    for path in paths:
        converted_path = []
        for point in path:
            converted_path.append(tuple(point.tolist()))
        converted_paths.append(tuple(converted_path))
    return converted_paths

def minimum_spanning_tree(converted_paths):
    all_points = set()
    for path in converted_paths:
        all_points.update(path)

    point_to_index = {}
    index_to_point = {}
    index = 0
    for point in all_points:
        point_to_index[point] = index
        index_to_point[index] = point
        index += 1

    edges = []
    for path in converted_paths:
        for i in range(len(path) - 1):
            u = point_to_index[path[i]]
            v = point_to_index[path[i + 1]]
            edges.append((u, v))

    edges.sort(key=lambda edge: len(set(edge)))

    n = len(all_points)
    tree = []
    uf = UnionFind(n)

    for u, v in edges:
        if uf.union(u, v):
            tree.append((index_to_point[u], index_to_point[v]))

    return tree

def add_random_edges_to_minimum_spanning_tree(minimum_spanning_tree, edges, salle_list):
    random_tree = minimum_spanning_tree.copy()
    free_edge = edges.copy()
    
    for room in list(salle_list.values()):
        pos = (room["position"][1],room["position"][2])
        count = len(room["connecteur"])
        for edge in minimum_spanning_tree:
            if pos == edge[0] or pos == edge[1]:
                count -= 1
        count = max(0,count)
        tentative = 0
        while count > 0:
            tentative += 1
            for edge in edges:
                if pos == edge[0] or pos == edge[1]:
                    random_tree.append(edge)
                    free_edge.remove(edge)
                    count -= 1
                    break
            edges = free_edge
            if tentative > 50:
                break

    return random_tree

def get_point(matrix, salle_list):

    # Récupération des coordonnées des points
    points = np.argwhere(matrix == 1)

    # Triangulation de Delaunay
    tri = Delaunay(points)

    edges = []

    # Parcourir chaque triangle
    for triangle in tri.simplices:
        # Générer toutes les arêtes possibles (combinaisons de deux points)
        # et les ajouter à la liste des arêtes
        edge1 = [points[triangle[0]], points[triangle[1]]]
        edge2 = [points[triangle[1]], points[triangle[2]]]
        edge3 = [points[triangle[2]], points[triangle[0]]]
        edges.extend([edge1, edge2, edge3])

    edges = convert_to_tuples(edges)
    tree = minimum_spanning_tree(edges)
    random_tree = add_random_edges_to_minimum_spanning_tree(tree, edges, salle_list)
    return random_tree



# Fonction pour calculer l'heuristique (distance de Manhattan) entre deux points
def calculate_heuristic(point, end):
    return abs(point[0] - end[0]) + abs(point[1] - end[1])

# Fonction pour vérifier si un point est valide dans la matrice
def is_valid_point(point, rows, cols):
    return 0 <= point[0] < rows and 0 <= point[1] < cols


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

def find_disconnected_points(matrice):
    y_max = len(matrice)
    x_max = len(matrice[0])
    z_max = len(matrice[0][0])

    validation = True
    for y in range(y_max):
        salle_valid,total_salle = [],0
        for x in range(x_max):
            for z in range(z_max):
                if matrice[y][x][z] != 0:
                    if matrice[y][x][z] == 1:
                        total_salle += 1

                    neighbors = [(y, x-1, z), (y, x+1, z), (y, x, z-1), (y, x, z+1)]

                    for neighbor in neighbors:
                        ny, nx, nz = neighbor
                        if 0 <= ny < y_max and 0 <= nx < x_max and 0 <= nz < z_max:
                            if matrice[y][x][z] == 1:
                                salle_valid.append((y,x,z))
                                break
        if len(salle_valid) != total_salle:
            validation = False
            print([len(salle_valid),total_salle])
    return validation

Instance = Donjon((20,20,20),(60,100))
Instance.Room_Type[1].append(RoomType("wood_5", "Salle de test",(1,1,2),np.array([[[1, 5, 1], [0, 1, 1], [0, 1, 1]],[[0, 0, 0], [0, 1, 1], [0, 1, 1]]]),filename = None))
Instance.Room_Type[0].append(RoomType("wood_2", "Salle de test",(1,1,2),np.array([[[5, 0, 5], [1, 1, 1], [0, 1, 0]]]),filename = None))
Instance.Generate(1)