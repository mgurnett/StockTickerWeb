import pickle
import json
from API_read import read_API

class Team:
    ''' The Team class for a single team '''
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.teamName = ""
        self.abbreviation = ""
        self.locationName = ""
        self.shortName = ""
        self.division = ""
        self.conference = ""
        self.venue = ""
        self.win = 0
        self.loss = 0
        self.otloss = 0
        self.points = 0
        self.games_played = 0
        self.point_percent = 0

    def __str__ (self):
        return (f'{self.name} of the {self.division} who play in {self.venue} and have played {self.games_played} games and have {self.points} points')
    
class AllTeams:
    ''' The class for all teams.  This is what gets pickeled. 
    print (AllTeams.__doc__)'''
    def __init__ (self, TeamObjects):
        self.teams = list(TeamObjects)

    def __str__ (self):
        for x in self.teams:
            print (x)

    def team_stats (self):
        for team in self.teams:
            url = (f'teams/{team.id}/stats')
            team_json = read_API (url)
            # packages_str = json.dumps (team_json['stats'][0]['splits'][0]['stat'], indent =2)
            # print (packages_str)
            team.games_played = team_json['stats'][0]['splits'][0]['stat']['gamesPlayed']
            team.win = team_json['stats'][0]['splits'][0]['stat']['wins']
            team.loss = team_json['stats'][0]['splits'][0]['stat']['losses']
            team.otloss = team_json['stats'][0]['splits'][0]['stat']['ot']
            team.points = team_json['stats'][0]['splits'][0]['stat']['pts']
            team.point_percent = team_json['stats'][0]['splits'][0]['stat']['ptPctg']

def load_teams ():
    '''load the teams data from the file if it is there, or get it from the API if it isn't.'''
    leag = []
    try:
        with open(f'teams.pickle', 'rb') as file:
            leag = pickle.load(file)
            print ('loaded teams from the file')
    except IOError:
        packages_json = read_API ('teams')
        team_list = []
        for index in range (len(packages_json['teams'])):
            team_id = packages_json['teams'][index]['id']
            current_team = Team (team_id)
            current_team.name = packages_json['teams'][index]['name']
            current_team.abbreviation = packages_json['teams'][index]['abbreviation']
            current_team.teamName = packages_json['teams'][index]['teamName']
            current_team.locationName = packages_json['teams'][index]['locationName']
            current_team.shortName = packages_json['teams'][index]['shortName']
            current_team.division = packages_json['teams'][index]['division']['name']
            current_team.venue = packages_json['teams'][index]['venue']['name']
            team_list.append (current_team)
            # print (current_team)

        leag = AllTeams (team_list)
        # for team in league.teams:
        #     print (team)

        with open(f'teams.pickle', 'wb') as file:
            pickle.dump(leag, file)
            print ('loaded teams from the API and then saved them to the file')
    return (leag)

if __name__ == '__main__':
    league = load_teams ()
    if league != []:
        for team in league.teams:
            packages_json = read_API ('teams')
        pass
    else:
        print ('FAILURE')

# print (AllTeams.__doc__)
# print (load_teams.__doc__)

league.team_stats()
print (league)
