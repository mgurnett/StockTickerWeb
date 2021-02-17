import requests

# Set up the API call variables
game_data = []
year = '2020'
season_type = '02' 
max_game_ID = 20
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
    
print (type(game_data))
one_game = game_data[18]
print(type(one_game))
# for x in one_game.keys():
#   print(x)
# for x in one_game.values():
#   print(x)
home = one_game['teams']['home']['team']['name']
h_score = one_game['teams']['home']['goals']
away = one_game['teams']['away']['team']['name']
a_score = one_game['teams']['away']['goals']
print (f'The {home} scored {h_score} and the {away} scored {a_score}')
  