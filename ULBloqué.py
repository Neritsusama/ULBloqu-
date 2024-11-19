# initialiser le jeu
#file_game
def parse_game(game_file_path: str) -> dict:
    if "+" in game_file_path :
        data = game_file_path.strip().split("\n") #dans le cas ou c'est un str et pas fichier
    else:
        with open(game_file_path, encoding="utf-8") as f:
            data = f.readlines()
    game = {}
    used_lines = [line.replace("|", "").strip() for line in data if '|' in line]
    game["width"] = len(used_lines[0])  
    game["height"] = len(used_lines)    
    game["cars"] = get_cars_draft(used_lines) #usage d'une fonction pour les voiture (plus propre)
    game["max_moves"] = int(data[-1].strip()) 

    return game

def get_cars_draft(map):
    cars_draft = {}
    for y, line in enumerate(map):
        for x, letter in enumerate(line):
            if letter.isalpha():  
                if letter not in cars_draft:
                    cars_draft[letter] = {'positions': []}
                cars_draft[letter]['positions'].append((x, y))
    cars = []
    for car, infos in sorted(cars_draft.items()): #lst des voitures triées
        positions = infos['positions']
        size = len(positions)
        if len(positions) > 1:
            if all(x == positions[0][0] for x, y in positions): #si mm x v sinon h
                orientation = 'v' 
            else:
                orientation = 'h' 
        cars.append([positions[0], orientation, size])
    return cars

#affichage

def get_game_str(game: dict, current_move_number: int) -> str:
    """
    Génère une chaîne de caractères représentant l'état actuel du plateau de jeu.

    Args:
        game (dict): Dictionnaire contenant les informations sur le jeu, incluant
                     les dimensions du plateau, les voitures et le nombre maximal de mouvements.
        current_move_number (int): Nombre actuel de mouvements effectués.

    Returns:
        str: Chaîne de caractères représentant le plateau de jeu et le nombre de mouvements effectués.
    """
    # Couleurs des voitures, dans l'ordre cyclique
    COLORS = [
        "\u001b[47m",  # Blanc pour A
        "\u001b[41m",  # Rouge
        "\u001b[42m",  # Vert
        "\u001b[43m",  # Jaune
        "\u001b[44m",  # Bleu
        "\u001b[45m",  # Magenta
        "\u001b[46m",  # Cyan
    ]
    
    grid = [['.' for _ in range(game["width"])] for _ in range(game["height"])]

    for i, car in enumerate(game["cars"]):
        position, orientation, size = car
        x, y = position
        color = COLORS[i % len(COLORS)]  # coul de la voiture, cyclique

        if orientation == 'h':  
            for i in range(size):
                grid[y][x + i] = f"{color}{car[0][0]}\u001b[0m"  
        elif orientation == 'v': 
            for i in range(size):
                grid[y + i][x] = f"{color}{car[0][0]}\u001b[0m"

    lines = ["+" + "-" * game["width"] + "+"]
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append("+" + "-" * game["width"] + "+")

    lines.append(f"Moves: {current_move_number}/{game['max_moves']}")

    return "\n".join(lines)

   
game = parse_game("game1.txt")
print(get_game_str(game, 40))
#séléction de la cars
#choix de la direction ou changement de de cars
#Vérification 
# Déplacement
# Vérification de la victoire
# Fin du jeu testtttt

