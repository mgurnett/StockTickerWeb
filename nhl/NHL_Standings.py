from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pretty_html_table import build_table

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 300
base_URL = "https://statsapi.web.nhl.com/api/v1/"

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
        
    def game_info(self):
        date = self.date.strftime("%a, %b %d, %y")
        game_string = f"{self.home_obj.name} played at home to the {self.away_obj.name} on {date}.  The game ended {self.home_score} - {self.away_score} {self.game_end}"
        return game_string
        
    def point_info(self):
        point_string = f"{self.home_obj.name} has {self.home_obj.points} and {self.away_obj.name} has {self.away_obj.points}"
        return point_string
    
    def games_recorded (self):
        if self.home_score > self.away_score:
            self.home_obj.win += 1
            if self.game_end == "OT":
                self.away_obj.otloss += 1
            elif self.game_end == "SO":
                self.away_obj.soloss += 1
            else:
                self.away_obj.loss += 1
        if self.home_score < self.away_score:
            self.away_obj.win += 1
            if self.game_end == "OT":
                self.home_obj.otloss += 1
            elif self.game_end == "SO":
                self.home_obj.soloss += 1
            else:
                self.home_obj.loss += 1
                
def read_API (section):
    url = base_URL + section
#     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        return print (f"status code is {r.status_code}")
    else:
        data = r.json()
        return data

def team_manager (team_id):
    global teams
    index = 0
    for i, t in enumerate(teams):
        if t.id == team_id:
            index = i
    if index == 0:
        teams.append (Team (team_id))
        index = len(teams)-1
    return (index)

            
    
teams = []; games = []
teams.append (Team (0))
        
# =======load the teams into the Class Teams===============
df_teams = read_API ("teams")
dict_teams = df_teams['teams']
for row in dict_teams:
    id = row['id']
    home_id = team_manager (id)
    teams [home_id].name = row['name']
    teams [home_id].teamName = row['teamName']
    teams [home_id].division = row['division']['name']
    teams [home_id].conference = row['conference']['name']
    teams [home_id].venue = row['venue']['name']
    teams [home_id].abbreviation = row['abbreviation']
#     teams [home_id].crazyname()

# print (teams[team_manager (22)].name_id())

# =======load the games into the Class Games===============
for i in range(1,max_game_ID):
    url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
    gameID = int(year + season_type +str(i).zfill(4)); #print (gameID)
    data = read_API (url)
    if data['currentPeriod'] != 0:
        home_id = (data['teams']['home']['team']['id'])
        away_id = (data['teams']['away']['team']['id'])
        date_data = data['periods'][0]['startTime']
        datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
        games.append ( Game (gameID, teams[team_manager (home_id)], teams[team_manager (away_id)], datetime_object))
        index = len(games)
        games[index-1].home_score = data['teams']['home']['goals']
        games[index-1].away_score = data['teams']['away']['goals']
        games[index-1].game_end = data['currentPeriodOrdinal']
        games[index-1].games_recorded()
        
game_frame = Team.standings('Scotia North')
#Scotia North,Honda West,Discover Central,MassMutual East, all
        
# print (game_frame.info()) 
# print (game_frame.head(10))
# print (game_frame.to_string())
# game_frame.plot.bar(x='Team', y='GP_adjust')
# plt.show()

html = game_frame.to_html()

# #write html to file
# text_file = open("index.html", "w")
# text_file.write(html)
# text_file.close()

html_table = build_table(game_frame, 'blue_dark')
# print(html_table_blue_light)

#write html to file
text_file = open("index.html", "w")
text_file.write(html_table)
text_file.close()