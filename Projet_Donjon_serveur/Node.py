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