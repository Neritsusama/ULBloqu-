# initialiser le jeu
def read_map(game_file):
    game = {}
    with open(game_file, encoding="utf-8") as f:
        data = f.readlines()
        game["widht"]= len(data[0][])
        game["height"] = len(data)

    return data, game["height"], game["widht"]
print(read_map("game1.txt"))
#file_game
#affichage
#séléction de la voiture
#choix de la direction ou changement de de voiture
#Vérification 
# Déplacement
# Vérification de la victoire
# Fin du jeu testtttt