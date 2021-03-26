import requests

class Game:
    def __init__ (self, id, home_obj, away_obj, date):
        self.id = id
        self.date = date
        self.home_obj = home_obj
        self.away_obj = away_obj
        self.home_score = 0
        self.away_score = 0
        self.game_end = ""
        self.home_point = 0
        self.away_point = 0
        self.future = True

class AllGames:
    def __init__ (self, GameObjects):

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