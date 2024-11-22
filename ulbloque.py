from getkey import getkey
from sys import argv

# initialiser le jeu
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

    if orientation == 'h': 
        for i in range(size):
            grid[y][x + i] = f"{color}{letter}\u001b[0m"
    elif orientation == 'v':
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
    y_exit = game["cars"][0][0][1]

    lines = [f"Moves: {current_move_number}/{game['max_moves']}"]
    lines.append("+" + "-" * game["width"] + "+")
    for y, row in  enumerate (grid):
        if y == y_exit :
            lines.append("|" + "".join(row) + "->")
        else :
            lines.append("|" + "".join(row) + "|")
    lines.append("+" + "-" * game["width"] + "+")

    return "\n".join(lines)

def select_car(game):
    car_letters = get_car_letter(game)

    while True:
        print(f"Choisissez une voiture parmi : {', '.join(car_letters)}")
        selected_letter = getkey().upper() 

        if selected_letter in car_letters:
            car_index = car_letters.index(selected_letter)
            return car_index
        else:
            print("Lettre invalide, essayez encore.")
            
def is_collision(game, car_index, new_positions):

    for other_car_index, other_car in enumerate(game["cars"]):
        if other_car_index == car_index:
            continue  # ignore la voiture en cours de déplacement

        # les cases occupées par l'autre voiture
        other_x, other_y = other_car[0]
        other_orientation = other_car[1]
        other_size = other_car[2]
        other_positions = []
        
        if other_orientation == "h": 
            other_positions = [(other_x + i, other_y) for i in range(other_size)]
        elif other_orientation == "v":  
            other_positions = [(other_x, other_y + i) for i in range(other_size)]

       
        if any(pos in other_positions for pos in new_positions):
            return True 
    return False  

def check_move(game, car_index, pos, direction):
    car = game["cars"][car_index]
    x, y = pos
    orientation = car[1]
    size = car[2]  

  
    if direction == "DOWN" and orientation == "v"  and (y + size) < game["height"]:
        y += 1
    elif direction == "UP" and orientation == "v" and (y - 1) >= 0:
        y -= 1
    elif direction == "LEFT" and orientation == "h" and (x - 1) >= 0:
        x -= 1
    elif direction == "RIGHT" and orientation == "h" and (x + size) < game["width"]:
        x += 1
    else:
        print("Mouvement impossible")
        return pos  

   
    new_positions = [
        (x + i, y) if car[1] == "h" else (x, y + i)
        for i in range(size)
    ]

    if is_collision(game, car_index, new_positions):
        print("Mouvement invalide : une autre voiture bloque le chemin.")
        return pos  
    
    game["cars"][car_index][0] = (x, y)
    return (x, y)


def move_car(game: dict, car_index: int, direction: str) -> bool :
    moved = False
    x, y = game["cars"][car_index][0]
    new_pos = check_move(game, car_index, (x, y), direction)
    if new_pos != (x, y):
        game["cars"][car_index][0] = new_pos
        moved = True
    return moved

def is_win(game: dict) -> bool:
    player_car_pos, orientation, size = game["cars"][0]
    #extremité v ou h
    if orientation == 'h':  
        car_end_pos = (player_car_pos[0] + size - 1, player_car_pos[1])
    elif orientation == 'v': 
        car_end_pos = (player_car_pos[0], player_car_pos[1] + size - 1)

    exit_pos = (game["width"] - 1, player_car_pos[1]) # sortie tjr sur la mm ligne mais dernière case

    return car_end_pos == exit_pos


def play_game(game) -> int:
    current_move = 0
    max_moves = game["max_moves"]  
    print(get_game_str(game, current_move))  
    selected_car_letter = None  
    car_index = None

    while not is_win(game):
        print("Appuyez sur une lettre pour choisir une voiture, utilisez les flèches pour la déplacer, ou ESCAPE pour abandonner.")
        input_key = getkey().upper() 
        car_letters = get_car_letter(game)

        if input_key == "ESCAPE":
            return QUIT
        
        if input_key in car_letters:
            selected_car_letter = input_key
            car_index = car_letters.index(selected_car_letter)
            print(f"Vous avez sélectionné la voiture : {selected_car_letter}")

        elif input_key in ["UP", "DOWN", "LEFT", "RIGHT"]:
            if selected_car_letter is None:
                print("Veuillez d'abord sélectionner une voiture.")
            elif move_car(game, car_index, input_key): 
                current_move += 1
                print(get_game_str(game, current_move)) 

                if is_win(game):
                    return WIN

                if current_move == max_moves:
                    return LOSE
        else:
            print("Touche invalide. Choisissez une lettre de voiture, une direction ou appuyez sur ESCAPE.")

    return WIN

def main():
    file_path = argv[1]
    game = parse_game(file_path)
    result = play_game(game)
    if result == WIN:
        print("Partie terminée : vous avez gagné !")
    elif result == LOSE:
        print("Partie terminée : vous avez perdu.")
    elif result == QUIT:
        print("Partie terminée : vous avez abandonné.")


if __name__ == "__main__":
    main()
