import requests
from datetime import datetime

# Set up the API call variables
game_data = []
year = '2020'
season_type = '02' 
max_game_ID = 30
base_URL = "https://statsapi.web.nhl.com/api/v1/"

def read_API (section):
    url = base_URL + section
    r = requests.get(url)
    if r.status_code != 200:
        return print (f"status code is {r.status_code}")
    else:
        data = r.json()
        return data

# Loop over the counter and format the API call
for i in range(1,max_game_ID):
    url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
    data = read_API (url)
    game_data.append(data)
    home = data['teams']['home']['team']['name']
    h_score = data['teams']['home']['goals']
    away = data['teams']['away']['team']['name']
    a_score = data['teams']['away']['goals']
    date_data = data['periods']
    try:
        date_data = data['periods'][0]['startTime']
    except:
      datetime_object = datetime.now()  
    date_data = data['periods'][0]['startTime']
    datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
    print (f'On {datetime_object.strftime("%a, %b %d")} the {home} scored {h_score} and the {away} scored {a_score}')
#     print (f'On the {home} scored {h_score} and the {away} scored {a_score}')
