import requests
import pandas as pd
'''
GET https://statsapi.web.nhl.com/api/v1/conferences Returns conference details
for all current NHL conferences.
API info - https://www.dataquest.io/blog/python-api-tutorial/
'''
URL = "https://statsapi.web.nhl.com/api/v1/"

class Conference ():
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.shortName = ""
        self.abbreviation = ""
        
    def crazyname (self):
        print (f"Conference name is {self.name} or {self.shortName} or {self.abbreviation} for short")

class Division ():
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.shortName = ""
        self.abbreviation = ""
        self.confer = ""
        
    def crazyname (self):
        print (f"Division name is {self.name} or {self.abbreviation} of the {self.confer}")

class Team ():
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
    
    

def read_API (section):
    responses = []
    url = URL + section
    response = requests.get(url)
    if response.status_code != 200:
        return print (f"status code is {response.status_code}")
    else:
        responses.append(response)
        r0 = responses[0]
        r0_json = r0.json()
        r0_section = r0_json[section]
#         print (r0_section)
        return pd.DataFrame(r0_section)

df_conf= read_API ("conferences")
conferences = []
for row in df_conf.iterrows():
    conf = Conference (row[1]['id'])
    conf.name = row[1]['name']
    conf.shortName = row[1]['shortName']
    conf.abbreviation = row[1]['abbreviation']
    conferences.append (conf)

# conferences[1].crazyname()

df_div= read_API ("divisions")
divisions = []
for row in df_div.iterrows():
    div = Division (row[1]['id'])
    div.name = row[1]['name']
    div.abbreviation = row[1]['abbreviation']
    divisions.append (div)

# divisions[3].crazyname()

df_team= read_API ("teams")
# print (df_team.info())
# print (df_team.head())
# print (df_team)
# teams = []
# for row in df_team.iterrows():
#     tm = Team (row[1]['id'])
#     tm.name = row[1]['name']
#     tm.teamName = row[1]['teamName']
#     tm.division = row[1]['division']['name']
#     tm.conference = row[1]['conference']['name']
#     tm.venue = row[1]['venue']['name']
#     tm.abbreviation = row[1]['abbreviation']
#     teams.append (tm)

# teams[20].crazyname()
# 
df_game= read_API ("games/2020020010")
# print (df_game.info())
# print (df_game.head())
# print (df_game)