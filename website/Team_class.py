import pickle
import json
import pandas as pd
from API_read import read_API

base_URL = "https://statsapi.web.nhl.com/api/v1/"

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
        self.roster = []

    def __str__ (self):
        return (f'{self.name} of the {self.division} who play in {self.venue} and have played {self.games_played} games and have {self.points} points')
    
    def print_roster (self):
        return (f'{self.name} have a roster of {self.roster}')
    
class AllTeams:
    ''' The class for all teams.  This is what gets pickeled. 
    print (AllTeams.__doc__)'''
    def __init__ (self, TeamObjects):
        self.teams = list(TeamObjects)

    def __str__ (self):
        for x in self.teams:
            print (x)
        
    @staticmethod
    def standings (teams, div):
        columns = ['Team', 'Games Played', 'Win', 'Loss', 'OT & SO Loss', 'points %', 'Points', 'Division']
        dummy = [['', 0, 0, 0, 0, 0, 0, '']]
        df = pd.DataFrame(columns=columns, data=dummy)
        for team in teams:
            data = (team.teamName, team.games_played,
                    team.win, team.loss,
                    team.otloss, team.point_percent,
                    team.points, team.division)
            a_series = pd.Series(data, index = df.columns)
            df = df.append(a_series, ignore_index=True)
        df = df.drop(0)
        
        if div == 'all':
            df = df.sort_values(by = 'Points', ascending = False)
        elif div in {'Scotia North', 'Honda West', 'Discover Central', 'MassMutual East'}:
            df = df [df['Division'] == div].sort_values(by = 'Points', ascending = False)
            
        max_gp = df['Games Played'].max()
        df ['GP_adjust'] = round((max_gp / df['Games Played'] * df['Points']), 1)
            
        df ['real_points'] = df['Win'] * 3 + df['OT & SO Loss']
        df = df.sort_values(by = 'GP_adjust', ascending = False)
        return df

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

    def convert_to_df (self):
        df = pd.DataFrame([team.__dict__ for team in self.teams ])
        # for team in self.teams:
        #     print (team)
        return df
    

def get_roster(t_id):
    roster = []
    active_roster = []
    url = (f'teams/{str(t_id)}/roster')
    data = read_API (url)
    roster_df = pd.json_normalize(data, ['roster'],  errors='ignore')
    # ; print (roster_df['person.id'])
    roster.append(roster_df['person.id'])
    for r in roster_df['person.id']:
        active_roster.append(r)
    return active_roster

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
        for index in range (len(packages_json['teams'])-1):
            team_id = packages_json['teams'][index]['id']
            current_team = Team (team_id)
            current_team.name = packages_json['teams'][index]['name']
            current_team.abbreviation = packages_json['teams'][index]['abbreviation']
            current_team.teamName = packages_json['teams'][index]['teamName']
            current_team.locationName = packages_json['teams'][index]['locationName']
            current_team.shortName = packages_json['teams'][index]['shortName']
            current_team.division = packages_json['teams'][index]['division']['name']
            current_team.venue = packages_json['teams'][index]['venue']['name']
            current_team.roster = get_roster (team_id)
            team_list.append (current_team)
            # print (current_team.print_roster())

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
    print (AllTeams.__doc__)
    print (load_teams.__doc__)
    # df = league.convert_to_df ()

    league.team_stats()
    # # print (league)
    print (AllTeams.standings(league.teams, 'Scotia North'))