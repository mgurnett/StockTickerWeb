import requests
from datetime import datetime

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 200
base_URL = "https://statsapi.web.nhl.com/api/v1/"

team_id_dict = {}

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
        self.date = ""
        self.home_goals = ""
        self.away_goals = ""
        self.date_played = ""

        # creating object of Employee class 
        self.home_obj = home_obj 
        self.away_obj = away_obj 
        
    def crazyname (self):
        print (f"The {self.name} or {self.teamName} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")
        
    def game_info (self):
        print (f"The {self.home_obj.name} were home to the {self.away_obj.name}")

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
for row in dict_teams:
    tm = Team (row['id'])
    dict_index = len(team_id_dict)
    team_id_dict [row['id']] = dict_index
    tm.name = row['name']
    tm.teamName = row['teamName']
    tm.division = row['division']['name']
    tm.conference = row['conference']['name']
    tm.venue = row['venue']['name']
    tm.abbreviation = row['abbreviation']
    
print (team_id_dict[22])
# =======load the games into the Class Games===============
# for i in range(1,max_game_ID):
#     url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
#     gameID = int(year + season_type +str(i).zfill(4)); #print (gameID)
#     data = read_API (url)
#     if data['currentPeriod'] != 0:
#         home_id = (data['teams']['home']['team']['id'])
#         home_team = Team (home_id)
#         print (home_team.teamName)
#         away_id = (data['teams']['away']['team']['id'])
#         away_team = Team (away_id)
#         print (away_team.teamName)
#         gm = Game (gameID, home_team, away_team)
#         
#         home = data['teams']['home']['team']['name']
#         h_score = data['teams']['home']['goals']
#         away = data['teams']['away']['team']['name']
#         a_score = data['teams']['away']['goals']
#         date_data = data['periods'][0]['startTime']
#         datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
#         print (f'On {datetime_object.strftime("%a, %b %d")} the {home} ({home_id}) scored {h_score} and the {away} ({away_id}) scored {a_score}')
#         
