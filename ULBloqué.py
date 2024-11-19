# initialiser le jeu
def parse_game(game_file_path):
    if "+" in game_file_path :
        data = game_file_path.strip().split("\n")
    else:
        with open(game_file_path, encoding="utf-8") as f:
            data = f.readlines()
    game = {}
    used_lines = [line.replace("|", "").strip() for line in data if '|' in line]
    game["width"] = len(used_lines[0])  
    game["height"] = len(used_lines)    
    game["cars"] = get_cars_draft(used_lines)
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
    for car, infos in sorted(cars_draft.items()):
        positions = infos['positions']
        size = len(positions)
        if len(positions) > 1:
            if all(x == positions[0][0] for x, y in positions):
                orientation = 'v' 
            else:
                orientation = 'h' 
        cars.append([positions[0], orientation, size])
    return cars





#file_game
#affichage
#séléction de la cars
#choix de la direction ou changement de de cars
#Vérification 
# Déplacement
# Vérification de la victoire
# Fin du jeu testtttt

