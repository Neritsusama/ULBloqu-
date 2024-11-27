"""
NOM : Raminahiarisoa
PRENOM : Aina Nathanaël
MATRICULE : 000591373
Date de remise : 15/12/2024
Projet :  ULBloqué : C’est un jeu à 1 joueur sur une grille donnée. Le but du jeu est de
          permettre à une voiture de sortir du parking en déplaçant les voitures qui lui bloquent
          la route.
"""

from getkey import getkey
from sys import argv

WIN = 0
LOSE = 1
QUIT = 2    
COLORS = [
        "\u001b[47m",  # Blanc 
        "\u001b[41m",  # Rouge
        "\u001b[42m",  # Vert
        "\u001b[43m",  # Jaune
        "\u001b[44m",  # Bleu
        "\u001b[45m",  # Magenta
        "\u001b[46m",  # Cyan
        ]


# ------------------------------------------------- Fonctions -------------------------------------------------


def parse_game(game_file_path: str) -> dict:
    """
    but : lire un fichier de jeu (ou une chaîne de caractères simulant un fichier) pour extraire les données
    """
    if "+" in game_file_path:                                   # vérifie si le chemin donné est une chaîne simulant un fichier comme pour le test
        data = game_file_path.strip().split("\n")               # divise la chaîne en lignes pour simuler un fichier
    else:
        with open(game_file_path, encoding="utf-8") as f:       # ouvre le fichier en mode lecture avec encodage utf-8
            data = f.readlines()                                # lit toutes les lignes du fichier et les stocke dans une liste
    game = {}                                                   # initialise un dictionnaire pour stocker les données du jeu
    used_lines = [line.replace("|", "").strip() for line in data if '|' in line]  
                                                                # supprime les caractères '|' et les espaces inutiles des lignes contenant un plateau
    game["width"] = len(used_lines[0])                          # largeur prenant la longueur d'une ligne
    game["height"] = len(used_lines)                            # hauteur comptant le nombre de lignes
    game["cars"] = get_cars_draft(used_lines)                   # récupère les informations des voitures 
    game["max_moves"] = int(data[-1].strip())                   # convertit la dernière ligne en entier pour le nombre maximal de déplacements

    return game                                                 # renvoie le dictionnaire contenant toutes les données du jeu


def get_cars_draft(map):
    """
    but : extraire les informations sur les voitures du plateau de jeu et les retourner sous forme de liste.
    """
    cars_draft = {}                                             
    for y, line in enumerate(map):                              # parcourt chaque ligne du plateau
        for x, letter in enumerate(line):                       # parcourt chaque lettre dans la ligne
            if letter.isalpha():                                # si la lettre est une lettre (voiture)
                if letter not in cars_draft:                    # si la voiture n'a pas encore été ajoutée
                    cars_draft[letter] = {'positions': []}      # crée une entrée pour la voiture
                cars_draft[letter]['positions'].append((x, y))  # ajoute la position de la voiture

    cars = []                                                   # initialise une liste pour les voitures finales
    for car, infos in sorted(cars_draft.items()):               # boucle sur les voitures triées par nom
        positions = infos['positions']                          # récupère les positions de la voiture
        size = len(positions)                                   # taille de la voiture (nombre de positions)
        if len(positions) > 1:                                  # si la voiture occupe plusieurs cases
            if all(x == positions[0][0] for x, y in positions): # si toutes les positions ont le même x
                orientation = 'v'                               # orientation verticale
            else:
                orientation = 'h'                               # sinon orientation horizontale
        cars.append([positions[0], orientation, size])          # ajoute la voiture à la liste
    return cars                                                 # renvoie la liste des voitures


def get_car_letter(game):
    """
    but : générer une liste des lettres représentant les voitures du jeu.
    """
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]   # crée une liste des lettres de l'alphabet
    return [alphabet[i] for i in range(len(game["cars"]))]       # retourne les lettres correspondant au nombre de voitures


def create_empty_grid(width: int, height: int) -> list:
    return [['.' for _ in range(width)] for _ in range(height)]


def add_car_to_grid(grid, car, letter, color):
    """
    but : ajouter une voiture sur le plateau en fonction de sa position, orientation et couleur.
    """
    position, orientation, size = car                           
    x, y = position                                             # extrait les coordonnées x et y de la position

    if orientation == 'h':                                      # si l'orientation est horizontale
        for i in range(size):                                   # parcourt la taille de la voiture
            grid[y][x + i] = f"{color}{letter}\u001b[0m"        # ajoute la voiture à chaque case horizontale
    elif orientation == 'v':                                    # si l'orientation est verticale
        for i in range(size):                                   # parcourt la taille de la voiture
            grid[y + i][x] = f"{color}{letter}\u001b[0m"        # ajoute la voiture à chaque case verticale


def add_all_cars_to_grid(game, grid, car_letters) :
    """
    but : ajouter toutes les voitures sur le plateau en fonction de leurs lettres, couleurs et informations.
    """
    color_cycle = COLORS[1:]                                    # liste des couleurs pour les voitures (en excluant la première couleur)
    white = COLORS[0]                                           # couleur blanche pour la première voiture (A)
    for i, car in enumerate(game["cars"]):                      # parcourt toutes les voitures du jeu
        letter = car_letters[i]                                 # récupère la lettre associée à la voiture
        if letter == 'A':                                       # si c'est la première voiture (A)
            color = white                                       # lui attribue la couleur blanche
        else:
            color = color_cycle[(i % len(color_cycle) - 1)]     # attribue une des couleurs cycliques aux autres voitures
        add_car_to_grid(grid, car, letter, color)               # ajoute la voiture au plateau avec la couleur et la lettre


def get_game_str(game: dict, current_move_number: int) -> str:
    """
    but : générer une chaîne représentant l'état actuel du jeu pour l'affichage.
    """
    car_letters = get_car_letter(game)                              # récupère les lettres des voitures
    grid = create_empty_grid(game["width"], game["height"])         # crée un plateau vide
    add_all_cars_to_grid(game, grid, car_letters)                   # ajoute toutes les voitures sur le plateau
    y_exit = game["cars"][0][0][1]                                  # récupère la position y de la voiture 'A' pour la sortie

    lines = [f"Moves: {current_move_number}/{game['max_moves']}"]   # ajoute l'information du nombre de mouvements
    lines.append("┌" + "─" * game["width"] + "┐")                   # ajoute une ligne de bordure en haut
    for y, row in enumerate(grid):                                  # boucle à travers chaque ligne du plateau               
        if y == y_exit :  
            lines.append("│" + "".join(row) + "-> EXIT")            # ajoute la flèche de sortie pour la voiture 'A'    
        else:            
            lines.append("│" + "".join(row) + "│")                  # ajoute une ligne normale du plateau
    lines.append("└" + "─" * game["width"] + "┘")                   # ajoute une ligne de bordure en bas

    return "\n".join(lines)                                         # renvoie la chaîne représentant l'état du jeu


def select_car(game):
    """
    but : permettre au joueur de sélectionner une voiture parmi celles disponibles.
    """
    car_letters = get_car_letter(game)                                      # récupère les lettres des voitures disponibles

    while True:  
        print(f"Choisissez une voiture parmi : {', '.join(car_letters)}")   # affiche les voitures disponibles
        selected_letter = getkey().upper()                                  # attend une entrée de l'utilisateur et la convertit en majuscule

        if selected_letter in car_letters:                                  # si la lettre sélectionnée est valide
            car_index = car_letters.index(selected_letter)                  # récupère l'index de la voiture sélectionnée
            return car_index                                                # renvoie l'index de la voiture


def is_collision(game, car_index, new_positions):
    """
    but : vérifier si un mouvement de voiture entraîne une collision avec une autre voiture.
    """
    collide = False                                                                         # initialise la variable de collision à False
    for other_car_index, other_car in enumerate(game["cars"]):                              # boucle sur toutes les voitures du jeu
        if other_car_index != car_index:                                                    # ignore la voiture en cours de déplacement
                                                                                            # récupère les coordonnées, orientation et taille de l'autre voiture
            other_x, other_y = other_car[0]
            other_orientation = other_car[1]
            other_size = other_car[2]
            other_positions = []

            if other_orientation == "h":                                                    # si l'orientation est horizontale
                other_positions = [(other_x + i, other_y) for i in range(other_size)]       # positions horizontales
            elif other_orientation == "v":                                                  # si l'orientation est verticale
                other_positions = [(other_x, other_y + i) for i in range(other_size)]       # positions verticales

            if any(pos in other_positions for pos in new_positions):                        # vérifie si collision avec les positions de l'autre voiture
                collide = True                                                              # il y a collision
    return collide                                                                          # renvoie si une collision a été détectée


def check_move(game, car_index, pos, direction):
    """
    but : vérifier si un mouvement proposé pour une voiture est valide, en tenant compte des limites du plateau et des collisions.
    """
    car = game["cars"][car_index]                                                   # récupère les informations de la voiture à déplacer
    x, y = pos                                                                      # récupère la position actuelle de la voiture
    orientation = car[1]                                                            # orientation de la voiture
    size = car[2]                                                                   # taille de la voiture

                                                                                    # détermine la nouvelle position 
    if direction == "DOWN" and orientation == "v" and (y + size) < game["height"]:
        y += 1                                                                      # déplace la voiture vers le bas si possible
    elif direction == "UP" and orientation == "v" and (y - 1) >= 0:
        y -= 1                                                                      # déplace la voiture vers le haut si possible
    elif direction == "LEFT" and orientation == "h" and (x - 1) >= 0:
        x -= 1                                                                      # déplace la voiture vers la gauche si possible
    elif direction == "RIGHT" and orientation == "h" and (x + size) < game["width"]:
        x += 1                                                                      # déplace la voiture vers la droite si possible
    else:
        print("Mouvement impossible")                                               # affiche un message d'erreur si le mouvement est invalide
        return pos                                                                  # retourne la position initiale si le mouvement est invalide
        
                                                                                    
    new_positions = [(x + i, y) if car[1] == "h" else (x, y + i) for i in range(size)] # calcule les nouvelles positions de la voiture après le mouvement
                                                                 
    if is_collision(game, car_index, new_positions):                                # vérifie s'il y a une collision
        print("Mouvement invalide : une autre voiture bloque le chemin.")           # message d'erreur en cas de collision
        return pos                                                                  # retourne la position initiale si collision
    game["cars"][car_index][0] = (x, y)                                             # met à jour la position de la voiture dans le jeu
    return (x, y)                                                                   # renvoie la nouvelle position de la voiture


def move_car(game, car_index: int, direction: str) -> bool:
    """
    but : déplacer une voiture selon la direction donnée si le mouvement est valide.
    """
    moved = False                                                                   # initialise une variable indiquant si le déplacement a eu lieu
    x, y = game["cars"][car_index][0]                                               # récupère la position actuelle de la voiture
    new_pos = check_move(game, car_index, (x, y), direction)                        # vérifie la validité du mouvement avec check_move
    if new_pos != (x, y):                                                           # si la nouvelle position est différente de l'ancienne, le mouvement est valide
        game["cars"][car_index][0] = new_pos                                        # met à jour la position de la voiture
        moved = True                                                                # marque que la voiture a été déplacée
    return moved                                                                    # renvoie si un déplacement a eu lieu ou non


def is_win(game: dict) -> bool:
    """
    but : vérifier si la voiture du joueur a atteint la sortie en bas à droite.
    """
    player_car_pos, orientation, size = game["cars"][0]                            # récupère la position, orientation et taille de la voiture du joueur
                                                                                   # calcule la position de l'extrémité de la voiture selon son orientation
    if orientation == 'h':  
        car_end_pos = (player_car_pos[0] + size - 1, player_car_pos[1])            # extrémité horizontale
    elif orientation == 'v': 
        car_end_pos = (player_car_pos[0], player_car_pos[1] + size - 1)            # extrémité verticale

    exit_pos = (game["width"] - 1, player_car_pos[1])                              # la position de la sortie est toujours sur la dernière colonne

    return car_end_pos == exit_pos                                                 # renvoie True si l'extrémité de la voiture est à la position de la sortie


def play_game(game : dict) -> int:
    """
    but : gérer le déroulement du jeu, permettre au joueur de déplacer ses voitures et vérifier si la victoire ou la défaite a été atteinte.
    """
    current_move = 0                                                                                                                # initialise le nombre de mouvements à 0
    max_moves = game["max_moves"]                                                                                                   # récupère le nombre maximal de mouvements autorisés
    print(get_game_str(game, current_move))                                                                                         # affiche l'état initial du jeu
    selected_car_letter = None                                                                                                      # variable pour stocker la lettre de la voiture sélectionnée
    car_index = None                                                                                                                # variable pour stocker l'index de la voiture sélectionnée

    while not is_win(game):                                                                                                         # continue tant que le joueur n'a pas gagné
        print("Appuyez sur une lettre pour choisir une voiture, utilisez les flèches pour la déplacer, ou ESCAPE pour abandonner.")
        input_key = getkey().upper()                                                                                                # attend l'entrée du joueur et la convertit en majuscule
        car_letters = get_car_letter(game)                                                                                          # récupère les lettres des voitures disponibles

        if input_key == "ESCAPE":                                                                                                   # permet au joueur d'abandonner à tout moment
            return QUIT
        
        if input_key in car_letters:                                                                                                # si le joueur choisit une voiture
            selected_car_letter = input_key
            car_index = car_letters.index(selected_car_letter)                                                                      # récupère l'index de la voiture choisie
            print(f"Vous avez sélectionné la voiture : {selected_car_letter}")

        elif input_key in ["UP", "DOWN", "LEFT", "RIGHT"]:                                                                          # si le joueur choisit une direction pour déplacer la voiture
            if selected_car_letter is None:                                                                                         # si aucune voiture n'est sélectionnée
                print("Veuillez d'abord sélectionner une voiture.")
            elif move_car(game, car_index, input_key):                                                                              # déplace la voiture si possible
                current_move += 1                                                                                                   # incrémente le nombre de mouvements
                print(get_game_str(game, current_move))                                                                             # affiche l'état du jeu après le mouvement

                if is_win(game):                                                                                                    # vérifie si le joueur a gagné après le déplacement
                    return WIN

                if current_move == max_moves:                                                                                       # vérifie si le joueur a atteint le nombre maximal de mouvements
                    print("Plus de mouvements disponibles.")                                                                                      
                    return LOSE
        else:                                                                                                                       
            print("Touche invalide. Choisissez une lettre de voiture, une direction ou appuyez sur ESCAPE.")                        # gestion des touches invalides

    return WIN                                                                                                                      # renvoie WIN si le joueur a gagné


# ------------------------------------------------- main -------------------------------------------------

def main():
    """
    but : lancer le jeu en initialisant le plateau à partir d'un fichier et gérer le résultat de la partie.
    """
    file_path = argv[1]                                 # récupère le chemin du fichier de jeu à partir des arguments de la ligne de commande
    game = parse_game(file_path)                        # initialise le jeu en lisant les données du fichier
    result = play_game(game)                            # lance la partie et récupère le résultat (WIN, LOSE, QUIT)
    
    if result == WIN:                                   # si le joueur a gagné
        print("Partie terminée : vous avez gagné !")
    elif result == LOSE:                                # si le joueur a perdu
        print("Partie terminée : vous avez perdu.")
    elif result == QUIT:                                # si le joueur a abandonné
        print("Partie terminée : vous avez abandonné.")

# ------------------------------------------------- corps du code -------------------------------------------------

if __name__ == "__main__":
    main()