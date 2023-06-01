import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from UnionFind import *

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