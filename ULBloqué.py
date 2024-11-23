from getkey import getkey
from sys import argv
import sys

# initialiser le jeu
COLORS = [
        "\u001b[47m",  # Blanc 
        "\u001b[41m",  # Rouge
        "\u001b[42m",  # Vert
        "\u001b[43m",  # Jaune
        "\u001b[44m",  # Bleu
        "\u001b[45m",  # Magenta
        "\u001b[46m",  # Cyan
        ]

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
def get_car_letter(game: dict) -> list: #j'ai pas les lettres dans game donc je les prends ici
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    return [alphabet[i] for i in range(len(game["cars"]))]

def create_empty_grid(width: int, height: int) -> list:
    return [['.' for _ in range(width)] for _ in range(height)]


def add_car_to_grid(grid: list, car: list, letter: str, color: str):
    position, orientation, size = car
    x, y = position

    if orientation == 'h':  # Horizontale
        for i in range(size):
            grid[y][x + i] = f"{color}{letter}\u001b[0m"
    elif orientation == 'v':  # Verticale
        for i in range(size):
            grid[y + i][x] = f"{color}{letter}\u001b[0m"

def add_all_cars_to_grid(game: dict, grid: list, car_letters: list) -> None:
    for i, car in enumerate(game["cars"]):
        letter = car_letters[i]
        color = COLORS[i % len(COLORS)]
        add_car_to_grid(grid, car, letter, color)

def get_game_str(game: dict, current_move_number: int) -> str:
    car_letters = get_car_letter(game)
    grid = create_empty_grid(game["width"], game["height"])
    add_all_cars_to_grid(game, grid, car_letters)

    lines = ["+" + "-" * game["width"] + "+"]
    for row in grid:
        lines.append("|" + "".join(row) + "|")
    lines.append("+" + "-" * game["width"] + "+")
    lines.append(f"Moves: {current_move_number}/{game['max_moves']}")

    return "\n".join(lines)

def select_car(game):
    car_letters = get_car_letter(game)

    while True:
        print(f"Choisissez une voiture parmi : {', '.join(car_letters)}")
        selected_letter = getkey().upper()  # Lecture de l'entrée et transformation en majuscule

        if selected_letter in car_letters:
            car_index = car_letters.index(selected_letter)
            return car_index
        else:
            print("Lettre invalide, essayez encore.")

def check_move(game, car_index, pos, direction):
    x, y = pos
    if direction == "DOWN" and 0 <= (y + 1) < game["height"]:
        y += 1
    elif direction == "UP" and 0 <= (y - 1) < game["height"]:
        y -= 1
    elif direction == "LEFT" and 0 <= (x - 1) < game["width"]:
        x -= 1
    elif direction == "RIGHT" and 0 <= (x + 1) < game["width"]:
        x += 1
    else : 
        print("Mouvement hors-limite")
    new_pos = (x, y)
    game["cars"][car_index][0] = new_pos
    return new_pos

def move_car(game: dict, car_index: int, direction: str) -> bool :
    moved = False
    x, y = game["cars"][car_index][0]
    new_pos = check_move(game, car_index, (x, y), direction)
    if check_move(game, car_index,(x, y), direction) != (x, y):
        game["cars"][car_index][0] = new_pos
        moved = True
    return moved

def choose_move() -> str:
    print("Choisissez une direction :")
    print("Flèches : UP, DOWN, LEFT, RIGHT")
    print("ESC : Terminer (mouvements continus)")
    
    while True:
        move = getkey().upper()  # Lecture de l'entrée utilisateur
        if move in ["UP", "DOWN", "LEFT", "RIGHT", "ESCAPE"]:  # Valide les entrées acceptées
            return move
        else:
            print("Entrée invalide. Essayez encore.")

   

def is_win(game: dict) -> bool:
    player_car_pos, orientation, size = game["cars"][0]

    #extremité v ou h
    if orientation == 'h':  
        car_end_pos = (player_car_pos[0] + size - 1, player_car_pos[1])
    elif orientation == 'v': 
        car_end_pos = (player_car_pos[0], player_car_pos[1] + size - 1)

    exit_pos = (game["width"] - 1, player_car_pos[1]) # sortie tjr sur la mm ligne mais dernière case

    return car_end_pos == exit_pos

def play_game(game: dict) -> int:
    print(get_game_str(game, 0))  # Affichage initial

    current_move_number = 0
    max_moves = game["max_moves"]

    """while True:
            move = select_tetramino(nb_pieces)
            movement(tetraminos, move, grid)
            while not is_win(game):
                move = select_tetramino(nb_pieces)
                movement(tetraminos, move, grid)
            print("Énigme résolue")

        if key == 'ESCAPE':
            print("Vous avez abandonné.")
            return 2  # Code d'abandon

        elif key in ["UP", "DOWN", "LEFT", "RIGHT"]:
            # Logique pour déplacer la voiture dans la direction donnée
            if move_car(game, car_index=0, direction=key):  # Exemple pour déplacer la première voiture
                current_move_number += 1

                

                if current_move_number >= max_moves:
                    print("Vous avez perdu. Nombre de mouvements dépassé.")
                    return 1  # Code de défaite

                print(get_game_str(game, current_move_number))
            else:
                print("Déplacement impossible.")
        else:
            print("Entrée invalide.")"""


current_move = 40
game = parse_game("game1.txt")
max_moves = game["max_moves"]
print(get_game_str(game, current_move))
while not is_win(game) :
    car_index = select_car(game)
    shift = choose_move()
    while not move_car(game,car_index, shift) and g
    move_car()
  
