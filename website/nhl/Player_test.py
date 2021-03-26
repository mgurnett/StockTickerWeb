class Player():
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.teamName = ""

    def __str__ (self):
        return (f'name= {self.name} playes for {self.teamName}')

class AllPlayers():
    def __init__ (self, PlayerObjects):
        self.players = list(PlayerObjects)

player_list = []
all_players = ['Michael','Darlene','Isaac','Isabelle','Rachelle','Michael','Max','Ellie']
for i, p in enumerate(all_players):
    current_player = Player (i)
    current_player.name = p
    print (current_player.name)
    player_list.append (current_player)

roster = AllPlayers (player_list)
for i in roster.players:
    print (i)
