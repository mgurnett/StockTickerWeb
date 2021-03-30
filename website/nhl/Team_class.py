import pickle
import json
import pandas as pd
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
        print (f'{self.name} of the {self.division}')
        return (f'{self.name} of the {self.division} who play in {self.venue} and have played {self.games_played} games and have {self.points} points')
    
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
        df = df.sort_values(by = 'GP_adjust', ascending = False)
        return df

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
# print (league)
print (AllTeams.standings(league.teams, 'Scotia North'))