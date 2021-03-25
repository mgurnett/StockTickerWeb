import requests

class Player():
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.teamName = ""

class AllPlayers():
    def __init__ (self, PlayerObjects):
        self.players = list(PlayerObjects)


class Single():
    def __init__(self, left, right):
        self.left=left
        self.right=right

class CollectionOfSingles():
    def __init__(self, SingleObjects):
        self.singles = list(SingleObjects) #the cast here is to indicate that some checks would be nice
        # Here is where you could put the save function like pickle.
        # https://stackoverflow.com/questions/30129109/array-of-class-objects-in-python-3-4/30129256#30129256


    
# class Skater (Player):
#     def __init__ (self, id):
#         super(). __init__ (self, id)

# class Goalie (Player):
#     def __init__ (self, id):
#         super(). __init__ (self, id)
if __name__ == '__main__':

    all_players = ['Michael','Darlene','Isaac','Isabelle','Rachelle','Michael','Max','Ellie']
    for i, p in enumerate(all_players):
        current_player = Player (i)
        current_player.name = p
        print (current_player.name)
        # roster = AllPlayers (current_player)

    # print (roster)

# class Team:
#     def __init__ (self, id):
#         self.id = id
#         self.name = ""
#         self.teamName = ""
#         self.abbreviation = ""
#         self.division = ""
#         self.conference = ""
#         self.venue = ""
#         self.win = 0
#         self.loss = 0
#         self.otloss = 0
#         self.soloss = 0
#         self.points = 0
#         self.games_played = 0

# class AllTeams:
#     def __init__ (self, TeamObjects):

# class Game:
#     def __init__ (self, id, home_obj, away_obj, date):
#         self.id = id
#         self.date = date
#         self.home_obj = home_obj
#         self.away_obj = away_obj
#         self.home_score = 0
#         self.away_score = 0
#         self.game_end = ""
#         self.home_point = 0
#         self.away_point = 0
#         self.future = True

# class AllGames:
#     def __init__ (self, GameObjects):

# class Division:
#     #class Cube will be an import

# class AllDivisions:
#     def __init__ (self, DivisioneObjects):

# def update_data ():  #this will go to the API and get all NEW data

# def save_class (obj, name):
#     with open(f'{name}.pickle', 'wb') as file:
#     pickle.dump(obj, file) 

# def load_class (name):
#     with open(f'{name}.pickle', 'rb') as file2:
#     obj = pickle.load(file2)
#     return object