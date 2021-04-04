import json
import requests
import pickle

# Set up the API call variables
year = '2020'
season_type = '02'
max_game_ID = 600
base_URL = "https://statsapi.web.nhl.com/api/v1/"

class Team:
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
        self.soloss = 0
        self.points = 0
        self.games_played = 0

    def __str__ (self):
        return (f'{self.name} of the {self.division} who play in {self.venue} and have played {self.games_played} games')
    
class AllTeams:
    def __init__ (self, TeamObjects):
        self.teams = list(TeamObjects)

def read_API(section):
    data = []
    url = base_URL + section
    r = requests.get(url)
    if r.status_code != 200:
        return print(f"status code is {r.status_code}")
    else:
        data = r.json()
        return data


if __name__ == '__main__':

    packages_json = read_API ('teams')
    packages_str = json.dumps (packages_json['teams'][0], indent =2)
    # print (packages_str)
    team_list = []
    for index in range (len(packages_json['teams'])):
        team_id = packages_json['teams'][index]['id']; print (team_id)
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

    league = AllTeams (team_list)
    for team in league.teams:
        print (team)

    with open(f'teams.pickle', 'wb') as file:
        pickle.dump(league, file)