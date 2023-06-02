import heapq
from Node import *
import random

# Fonction pour calculer l'heuristique (distance de Manhattan) entre deux points
def calculate_heuristic(point, end):
    return abs(point[0] - end[0]) + abs(point[1] - end[1])

# Fonction pour vérifier si un point est valide dans la matrice
def is_valid_point(point, rows, cols):
    return 0 <= point[0] < rows and 0 <= point[1] < cols

# Fonction de recherche du chemin le plus court
def find_shortest_path(matrix, start, end):
    rows = len(matrix)
    cols = len(matrix[0])

    # Vérifier si les points de départ et d'arrivée sont valides
    if not is_valid_point(start, rows, cols) or not is_valid_point(end, rows, cols):
        print("Invalide A")
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
                print(f"Reussite de la recherche entre {start} et {end}")
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
    print(f"Echec de la recherche entre {start} et {end}")
    # Aucun chemin trouvé
    return None

def find_disconnected_points(matrice):
    pass