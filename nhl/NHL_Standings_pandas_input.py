from datetime import datetime
import requests
import pandas as pd
# import json

from pretty_html_table import build_table

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 300
base_URL = "https://statsapi.web.nhl.com/api/v1/"

def make_web (name, df):
    html_table = build_table(df, 'blue_dark')
    file_name = ('games_folder/' + name + ".html")
    text_file = open(file_name, "w")
    text_file.write(html_table)
    text_file.close()
'''
url = base_URL + 'teams'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    teams_df = pd.json_normalize(data, ['teams'], errors='ignore')
#     print (teams_df.info())
    make_web ('teams', teams_df)

# url = base_URL + 'venues'    USELESS
# #     print (url)
# r = requests.get(url)
# if r.status_code != 200:
#     print (f"status code is {r.status_code}")
# else:
#     data = r.json()
#     venues_df =  pd.json_normalize(data, ['venues'], errors='ignore')
# #     print (venues_df.info())
# #     print (venues_df)
#     make_web ('venues', venues_df)

url = base_URL + 'standings'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    standings_df =  pd.json_normalize(data, ['records'], errors='ignore')
    
    sub_list = standings_df.iloc[0]['teamRecords']
    sub_df = pd.DataFrame(sub_list)
#     print (sub_df.info())
#     print (sub_df)

    make_web ('standings', sub_df)

games_list = []
for i in range(1,max_game_ID):
    url = base_URL + 'game/' + year + season_type +str(i).zfill(4) + '/linescore'
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        games_df =  pd.json_normalize(data, [0], errors='ignore')
        games_list.append(games_df)

all_games = pd.DataFrame(games_list)
make_web ('games', all_games)
'''

games_list = []
for i in range(1, 30):
    url = base_URL + 'game/' + year + season_type +str(i).zfill(4) + '/linescore'
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        games_df =  pd.json_normalize(data, errors='ignore')
        if games_df['currentPeriod'][0] > 0: 
            if games_df['hasShootout'][0]:
#                 print (games_df['shootoutInfo.startTime'][0])
               games_df = games_df.drop(columns=['shootoutInfo.startTime'])
#             print (games_df['currentPeriod'][0])
#             print (games_df.info())
            games_list.append(games_df)
#             name = 'games' + str(i)
#             make_web (name, games_df)

print (games_list)
all_games = pd.DataFrame(games_list)
make_web ('games', all_games)

# 