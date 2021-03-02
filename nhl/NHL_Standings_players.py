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
    
def get_teams ():    
    team_id = []
    url = base_URL + 'teams'
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        teams_df = pd.json_normalize(data, ['teams'], errors='ignore')
        team_id = teams_df['id']
    #     print (team_id)
    #     make_web ('teams', teams_df)
    return team_id

def get_rosters (t_id):
    roster = []; active_roster = []
    for team in t_id:
        url = base_URL + '/teams/' + str(team) + '/roster'
    #     print (url)
        r = requests.get(url)
        if r.status_code != 200:
            print (f"status code is {r.status_code}")
        else:
            data = r.json()
            roster_df = pd.json_normalize(data, ['roster'],  errors='ignore')
            roster.append (roster_df['person.id'])#; print (roster_df['person.id'])
            for r in roster_df['person.id']:
                active_roster.append (r)
    return active_roster

def get_player_data (url):
#     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
    return data

def get_player_info (id):
    #Player stats
    url = base_URL + '/people/' + str(id) + '/stats?stats=statsSingleSeason&season=20202021'
    data = get_player_data (url) # data is a <class 'dict'>
    data_stats = data['stats'][0]#; print ('data_stats', type(data_stats), data_stats)
    data_splits = data_stats['splits']#; print ('data_splits', type(data_splits), data_splits)
    
    if data_splits != []:
        data_splits = data_stats['splits'][0]#; print ('data_splits', type(data_splits), data_splits)
        data_stat = data_splits['stat']#; print ('data_stat', type(data_stat), data_stat.keys())
        player_stats_dict = {'points': data_stat.get('points'),
                             'goals': data_stat.get('goals'),
                             'pim': data_stat.get('pim'),
                             'shots': data_stat.get('shots'),
                             'games': data_stat.get('games'),
                             'powerPlayGoals': data_stat.get('powerPlayGoals'),
                             'powerPlayPoints': data_stat.get('powerPlayPoints'),
                             'penaltyMinutes': data_stat.get('penaltyMinutes'),
                             'plusMinus': data_stat.get('plusMinus'),
                             'points': data_stat.get('points') }
#         print (player_stats_dict)
        url = base_URL + '/people/' + str(id)
        data = get_player_data (url)#; print ('data', type(data), data)
        data_people = data['people'][0]#; print ('data_people', type(data_people), data_people)
#         print (data_people.keys())#; print ('data_splits', type(data_splits), data_splits)
        player_info_dict = {'id': data_people.get('id'),
                            'firstName': data_people.get('firstName'),
                            'lastName': data_people.get('lastName'),
                            'primaryNumber': data_people.get('primaryNumber'),
                            'currentAge': data_people.get('currentAge'),
                            'nationality': data_people.get('nationality'),
                            'active': data_people.get('active'),
                            'alternateCaptain': data_people.get('alternateCaptain'),
                            'captain': data_people.get('captain'),
                            'rosterStatus': data_people.get('rosterStatus'),
                            'currentTeam.id': data_people.get('currentTeam.id'),
                            'primaryPosition.name': data_people.get('primaryPosition.name')  }
        player_info_dict.update(player_stats_dict)#; print ('player_info_dict', type(player_info_dict), player_info_dict)
#         print (player_info_dict.keys())
        all_players_df = pd.DataFrame(player_info_dict, index=['i',])

    else:
        all_players_df = []
    return all_players_df
        
team_ids = get_teams(); print (f'Got the team ids for {len(team_ids)} teams')
roster_ids = get_rosters (team_ids); print (f'Got the team roster ids for {len(roster_ids)} players')

all_players_df = pd.DataFrame(columns=['id', 'firstName', 'lastName', 'primaryNumber',
                                       'currentAge', 'nationality', 'active', 'alternateCaptain',
                                       'captain', 'rosterStatus', 'currentTeam.id',
                                       'primaryPosition.name', 'points', 'goals', 'pim',
                                       'shots', 'games', 'powerPlayGoals', 'powerPlayPoints',
                                       'penaltyMinutes', 'plusMinus'])
for i, r in enumerate(roster_ids):
    print (i)
    player_stats_df = (get_player_info (r))#; print ('player_stats_df', type(player_stats_df), player_stats_df)
    all_players_df = all_players_df.append(player_stats_df)#; print ('all_players_df', type(all_players_df), all_players_df)
make_web ('players', all_players_df)