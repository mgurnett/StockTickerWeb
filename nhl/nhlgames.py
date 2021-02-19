import requests
from datetime import datetime

# Set up the API call variables
game_data = []
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
        self.division = ""
        self.conference = ""
        self.venue = ""
        
    def crazyname (self):
        print (f"The {self.name} or {self.teamName} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")

class Game:
    def __init__ (self, id, home_obj, away_obj):
        self.id = id
        self.name = ""
        self.teamName = ""
        self.abbreviation = ""
        self.division = ""
        self.conference = ""
        self.venue = ""

        # creating object of Employee class 
        self.home_obj = home_obj 
        self.away_obj = away_obj 
        
    def crazyname (self):
        print (f"The {self.name} or {self.teamName} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")
        
    def game_info (self):
        print (f"The {self.home_obj} were home to the {self.away_obj} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")

def read_API (section):
    url = base_URL + section
#     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        return print (f"status code is {r.status_code}")
    else:
        data = r.json()
        return data
        
# =======load the teams into the Class Teams===============
df_teams = read_API ("teams")
dict_teams = df_teams['teams']
teams = []
for row in dict_teams:
    tm = Team (row['id'])
    tm.name = row['name']
    tm.teamName = row['teamName']
    tm.division = row['division']['name']
    tm.conference = row['conference']['name']
    tm.venue = row['venue']['name']
    tm.abbreviation = row['abbreviation']
    teams.append (tm)
        
# =======load the games into the Class Games===============

for i in range(1,max_game_ID):
    url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
    gameID = int(year + season_type +str(i).zfill(4)); print (gameID)
    data = read_API (url)
    game_data.append(data)
    if data['currentPeriod'] != 0:    
        home = data['teams']['home']['team']['name']
        h_score = data['teams']['home']['goals']
        away = data['teams']['away']['team']['name']
        a_score = data['teams']['away']['goals']
        date_data = data['periods'][0]['startTime']
        datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
        print (f'On {datetime_object.strftime("%a, %b %d")} the {home} scored {h_score} and the {away} scored {a_score}')

