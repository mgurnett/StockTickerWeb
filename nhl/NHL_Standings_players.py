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
        print (data_stat.keys())
        print ('============')
#     players_stats_df = pd.json_normalize(data, ['stats'], errors='ignore')
#     if players_stats_df['splits'][0] != []:
#         temp_df = players_stats_df['splits'][0][0]['stat']
#         url = base_URL + '/people/' + str(id)
#         data = get_player_data (url)
#         players_info_df = pd.json_normalize(data, ['people'], errors='ignore')
#         
#         temp_df = pd.DataFrame.from_dict(temp, orient='index')
#             temp2_df = temp_df.transpose()
#         
#         player_info_dict = {'id': players_info_df['id'],
#                             'firstName': players_info_df['firstName'],
#                             'lastName': players_info_df['lastName'],
#                             'primaryNumber': players_info_df['primaryNumber'],
#                             'currentAge': players_info_df['currentAge'],
#                             'nationality': players_info_df['nationality'],
#                             'active': players_info_df['active'],
#                             'alternateCaptain': players_info_df['alternateCaptain'],
#                             'captain': players_info_df['captain'],
#                             'rosterStatus': players_info_df['rosterStatus'],
#                             'currentTeam.id': players_info_df['currentTeam.id'],
#                             'primaryPosition.name': players_info_df['primaryPosition.name']  }
#         
#         player_stats_dict = {'assists': temp2_df['assists'],
#                                 'goals': temp2_df['goals'],
#                                 'pim': temp2_df['pim'],
#                                 'shots': temp2_df['shots'],
#                                 'games': temp2_df['games'],
#                                 'powerPlayGoals': temp2_df['powerPlayGoals'],
#                                 'powerPlayPoints': temp2_df['powerPlayPoints'],
#                                 'penaltyMinutes': temp2_df['penaltyMinutes'],
#                                 'plusMinus': temp2_df['plusMinus'],
#                                 'points': temp2_df['points'] }
# 
#             temp3_df = pd.DataFrame.from_dict(player_part_dict, orient='index')
# 
#     player_details = pd.concat([player_info_df, temp3_df], axis=1)
#     return player_details
    return data
        
team_ids = get_teams(); print (f'Got the team ids for {len(team_ids)} teams')
roster_ids = get_rosters (team_ids); print (f'Got the team roster ids for {len(roster_ids)} players')

# player_stats =[]
for i, r in enumerate(roster_ids):
    print (i)
    player_stats = (get_player_info (r))
#     print (get_player_info (r))
#     if i == 20:
# #         print (player_stats)
#         all_players = pd.DataFrame(player_stats)
#         make_web ('players', all_players)