from datetime import datetime
import requests
import pandas as pd
import json 

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 300
base_URL = "https://statsapi.web.nhl.com/api/v1/"

'''
url = base_URL + 'teams'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    teams_df = pd.json_normalize(data, ['teams'], errors='ignore')
    print (teams_df.info())

url = base_URL + 'venues'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    venues_df =  pd.json_normalize(data, ['venues'], errors='ignore')
    print (venues_df.info())
    print (venues_df)

url = base_URL + 'standings'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    standings_df =  pd.json_normalize(data, ['records'], errors='ignore')
    print (standings_df.info())
    print (standings_df)
'''

url = base_URL + 'schedule?season=20202021'
#     print (url)
r = requests.get(url)
if r.status_code != 200:
    print (f"status code is {r.status_code}")
else:
    data = r.json()
    schedule_df =  pd.json_normalize(data, errors='ignore')
    print (schedule_df.info())
    print (schedule_df)
    
    

    
'''
for i in range(1,max_game_ID):
    url = base_URL + 'game/' + year + season_type +str(i).zfill(4) + '/linescore'
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        teams_df = pd.json_normalize(data, errors='ignore')
#         print (teams_df.info())
'''