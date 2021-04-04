import requests

class Player:
    def __init__ (self, id):
        self.id = id
        self.firstName = ""
        self.lastName = ""
        self.primaryNumber = 0
        self.currentAge = 0
        self.nationality = ""
        self.alternateCaptain = False
        self.captain = False
        self.rosterStatus = ""
        self.currentTeam = ""
        self.primaryPosition_name = ""
        # self.fullName = self.full_name()

    def __str__ (self):
        return (f'{self.full_name()} plays for {self.currentTeam}')

    def full_name (self):
        # print (f'firstName {self.firstName}')
        n = (f'{self.firstName} {self.lastName}')
        # print (self.firstName, n)
        return n

class Skater (Player):
    def __init__ (self, id):
        super(). __init__ (self, id)

        self.points = 0
        self.goals = 0
        self.assists = 0
        self.pim = 0
        self.shots = 0
        self.games = 0
        self.powerPlayGoals = 0
        self.powerPlayPoints = 0
        self.penaltyMinutes = 0
        self.plusMinus = 0

class Goalie (Player):
    def __init__ (self, id):
        super(). __init__ (self, id)

        self.games = 0

class AllPlayers:
    def __init__ (self, PlayerObjects):
        self.players = list(PlayerObjects)


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

if __name__ == '__main__':

    player_list = []
    all_players = ['Michael','Darlene','Isaac','Isabelle','Rachelle','Michael','Max','Ellie']
    for i, p in enumerate(all_players):
        current_player = Player (i)
        current_player.firstName = p
        # print (current_player.full_name())
        player_list.append (current_player)

    roster = AllPlayers (player_list)
    for i in roster.players:
        print (i)