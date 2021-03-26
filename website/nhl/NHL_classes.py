import requests

class Team:
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.teamName = ""
        self.abbreviation = ""
        self.division = ""
        self.conference = ""
        self.venue = ""
        self.win = 0
        self.loss = 0
        self.otloss = 0
        self.soloss = 0
        self.points = 0
        self.games_played = 0

    def __str__ (self):
        return (f'{self.teamName} of the {self.division} who play in {self.venue} and have played {self.games_played} games')

class AllTeams:
    def __init__ (self, TeamObjects):
        self.teams = list(TeamObjects)



if __name__ == '__main__':

    team_list = []
    all_teams = ['Oilers','Flames','Maple Leafs','Canucks','Seniters','Canadian']
    for i, p in enumerate(all_players):
        current_player = Player (i)
        current_player.firstName = p
        # print (current_player.full_name())
        player_list.append (current_player)

    roster = AllPlayers (player_list)
    for i in roster.players:
        print (i)