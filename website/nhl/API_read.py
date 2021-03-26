import json
import requests

# Set up the API call variables
year = '2020'
season_type = '02'
max_game_ID = 600
base_URL = "https://statsapi.web.nhl.com/api/v1/"

def read_API(section):
    data = []
    url = base_URL + section
    r = requests.get(url)
    if r.status_code != 200:
        return print(f"status code is {r.status_code}")
    else:
        data = r.json()
        return data

 

if __name__ == '__main__':
    packages_json = read_API ('teams')
    packages_str = json.dumps (packages_json['teams'][0], indent =2)
    # print (packages_str)
    team_name = packages_json['teams'][0]['name']; print (team_name)
    team_id = packages_json['teams'][0]['id']; print (team_id)