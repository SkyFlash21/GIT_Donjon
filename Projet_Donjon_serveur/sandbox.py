import random

# Dimensions de la grille du donjon
GRID_WIDTH = 20
GRID_HEIGHT = 20
GRID_DEPTH = 3

# Liste des presets de salle (représentés par leur taille)
room_presets = [
    (3, 2),  # (largeur, hauteur) de la salle
    (2, 2),
    (4, 3),
    # Ajoutez ici d'autres presets de salle
]

def generate_dungeon():
    # Création de la grille du donjon
    dungeon = [[[None for _ in range(GRID_DEPTH)] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    visited = set()

    # Fonction pour vérifier si une salle est valide (dans les limites de la grille et non visitée)
    def is_valid_room(x, y, z, width, height):
        for i in range(width):
            for j in range(height):
                if not (0 <= x + i < GRID_WIDTH and 0 <= y + j < GRID_HEIGHT and (x + i, y + j, z) not in visited):
                    return False
        return True

    # Fonction pour ajouter une salle à la grille du donjon
    def add_room(x, y, z, width, height, room):
        for i in range(width):
            for j in range(height):
                dungeon[x + i][y + j][z] = room
                visited.add((x + i, y + j, z))

    # Fonction pour obtenir les salles voisines d'une position donnée
    def get_neighboring_rooms(x, y, z, width, height):
        neighbors = []
        for i in range(width):
            if is_valid_room(x + i - 1, y, z, 1, height):
                neighbors.append((x + i - 1, y, z))
            if is_valid_room(x + i + 1, y, z, 1, height):
                neighbors.append((x + i + 1, y, z))
        for j in range(height):
            if is_valid_room(x, y + j - 1, z, width, 1):
                neighbors.append((x, y + j - 1, z))
            if is_valid_room(x, y + j + 1, z, width, 1):
                neighbors.append((x, y + j + 1, z))
        return neighbors

    # Sélectionne une salle de départ aléatoirement et l'ajoute au donjon
    start_x = random.randint(0, GRID_WIDTH - 1)
    start_y = random.randint(0, GRID_HEIGHT - 1)
    start_z = random.randint(0, GRID_DEPTH - 1)
    start_width, start_height = random.choice(room_presets)
    add_room(start_x, start_y, start_z, start_width, start_height, "Start")

    # Liste des salles à visiter
    rooms_to_visit = [(start_x, start_y, start_z, start_width, start_height)]

    # Parcours du donjon
    while rooms_to_visit:
        current_room = rooms_to_visit.pop()
        x, y, z, width, height = current_room
        neighbors = get_neighboring_rooms(x, y, z, width, height)

        if neighbors:
            next_x, next_y, next_z = random.choice(neighbors)
            next_width, next_height = random.choice(room_presets)
            add_room(next_x, next_y, next_z, next_width, next_height, "Room")
            rooms_to_visit.append((next_x, next_y, next_z, next_width, next_height))

    return dungeon

# Exemple d'utilisation
dungeon = generate_dungeon()
for z in range(GRID_DEPTH):
    print(f"Level {z + 1}:")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            print(dungeon[x][y][z] or "Empty", end=" ")
        print()
    print()
