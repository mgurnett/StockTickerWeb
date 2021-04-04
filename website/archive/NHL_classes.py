from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 600
base_URL = "https://statsapi.web.nhl.com/api/v1/"

teams = []; games = []

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
        self.game_played = 0
        
    @staticmethod
    def standings (div):
        columns = ['Team', 'Games Played', 'Win', 'Loss', 'OT Loss', 'SO Loss', 'Points', 'Division']
        dummy = [['', 0, 0, 0, 0, 0, 0, '']]
        df = pd.DataFrame(columns=columns, data=dummy)
        for team in teams:
            if team.name:  #see if the team is empty
                team.game_points()
                data = (team.name, team.game_played,
                        team.win, team.loss,
                        team.otloss, team.soloss,
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
    
    def name_id (self):
        namestring = f"The team is {self.name} with id of {self.id}"
        return namestring
        
    def crazyname (self):
        print (f"The {self.name} or {self.teamName} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")
        
    def game_points (self):
        self.points = self.win * 2 + self.otloss + self.soloss
        self.game_played = self.win + self.otloss + self.soloss + self.loss
        
        
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
        
    def game_info(self):
        date = self.date.strftime("%a, %b %d, %y")
        game_string = f"{self.home_obj.name} played at home to the {self.away_obj.name} on {date}.  The game ended {self.home_score} - {self.away_score} {self.game_end}"
        return game_string
        
    def game_dict(self):
        if self.home_score > self.away_score:
            self.home_point = 2
            if self.game_end == "OT":
                self.away_point = 1
            elif self.game_end == "SO":
                self.away_point = 1
            else:
                self.away_point = 0
        if self.home_score < self.away_score:
            self.away_point = 2
            if self.game_end == "OT":
                self.home_point = 1
            elif self.game_end == "SO":
                self.home_point = 1
            else:
                self.home_point = 0 
            
        date = str(self.date.strftime("%b %d, %y"))
        g_dict = {'home_team': self.home_obj.name,
                  'away_team': self.away_obj.name,
                  'home_score': self.home_score,
                  'away_score': self.away_score,
                  'date': self.date,
                  'home_point': self.home_point,
                  'away_point': self.away_point,
                  'Division': self.home_obj.division, }
        return g_dict
        
    def point_info(self):
        point_string = f"{self.home_obj.name} has {self.home_obj.points} and {self.away_obj.name} has {self.away_obj.points}"
        return point_string
    
    def games_recorded (self):
        if self.home_score > self.away_score:
            self.home_obj.win += 1
            if self.game_end == "OT":
                self.away_obj.otloss += 1
            elif self.game_end == "SO":
                self.away_obj.otloss += 1
            else:
                self.away_obj.loss += 1
        if self.home_score < self.away_score:
            self.away_obj.win += 1
            if self.game_end == "OT":
                self.home_obj.otloss += 1
            elif self.game_end == "SO":
                self.home_obj.otloss += 1
            else:
                self.home_obj.loss += 1
