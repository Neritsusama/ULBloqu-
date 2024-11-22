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
    new_pos = (x, y)
    game["cars"][car_index][0] = new_pos
    return new_pos

def move_car(game: dict, car_index: int, direction: str) -> bool :
    moved = False
    x, y = game["cars"][car_index][0]
    if check_move(game, car_index,(x, y), direction) != (x, y):
        moved = True
    return moved

def is_win(game: dict) -> bool:
    player_car_pos, orientation, size = game["cars"][0]
    if orientation == 'h':  
        car_end_pos = (player_car_pos[0] + size - 1, player_car_pos[1])
    elif orientation == 'v': 
        car_end_pos = (player_car_pos[0], player_car_pos[1] + size - 1)
        
    exit_pos = (game["width"] - 1, player_car_pos[1])

    return car_end_pos == exit_pos
