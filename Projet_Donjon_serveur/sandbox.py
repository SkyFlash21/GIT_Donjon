import random

def generate_3d_array(dim_x, dim_y, dim_z):
    array_3d = []
    for _ in range(dim_x):
        plane = []
        for _ in range(dim_y):
            row = []
            for _ in range(dim_z):
                row.append(random.choice([0, 1, 3, 5]))  # Valeurs aléatoires dans l'array 3D
            plane.append(row)
        array_3d.append(plane)
    return array_3d

def get_valid_neighbors(array, x, y, z):
    valid_neighbors = []
    neighbor_offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    for offset in neighbor_offsets:
        neighbor_x = x + offset[0]
        neighbor_y = y + offset[1]
        neighbor_z = z + offset[2]
        if (
            0 <= neighbor_x < len(array) and
            0 <= neighbor_y < len(array[neighbor_x]) and
            0 <= neighbor_z < len(array[neighbor_x][neighbor_y]) and
            array[neighbor_x][neighbor_y][neighbor_z] != 0
        ):
            valid_neighbors.append((neighbor_x, neighbor_y, neighbor_z))
    return valid_neighbors

def explore_array(array):
    dim_x = len(array)
    dim_y = len(array[0])
    dim_z = len(array[0][0])
    visited = set()
    start_x = random.randint(0, dim_x - 1)
    start_y = random.randint(0, dim_y - 1)
    start_z = random.randint(0, dim_z - 1)
    stack = [(start_x, start_y, start_z)]
    connected = set()
    separated = set()

    while stack:
        x, y, z = stack.pop()
        if (x, y, z) in visited:
            continue
        visited.add((x, y, z))

        if array[x][y][z] != 0:
            connected.add((x, y, z))
            neighbors = get_valid_neighbors(array, x, y, z)
            for neighbor in neighbors:
                stack.append(neighbor)
        else:
            separated.add((x, y, z))

    return connected, separated

# Exemple d'utilisation
array_3d = generate_3d_array(5, 5, 5)
connected_values, separated_values = explore_array(array_3d)

print("Valeurs connectées :")
for value in connected_values:
    print(value)

print("\nValeurs séparées :")
for value in separated_values:
    print(value)