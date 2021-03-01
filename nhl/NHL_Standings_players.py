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

def get_player_info (id):
    url = base_URL + '/people/' + str(id)
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        players_df_full = pd.json_normalize(data, ['people'], errors='ignore')
#         make_web ('players' + str(id), players_df_full)
#         print (players_df_full.info())
        player_part_dict = {'id': players_df_full['id'],
                            'firstName': players_df_full['firstName'],
                            'lastName': players_df_full['lastName'],
                            'primaryNumber': players_df_full['primaryNumber'],
                            'currentAge': players_df_full['currentAge'],
                            'nationality': players_df_full['nationality'],
                            'active': players_df_full['active'],
                            'alternateCaptain': players_df_full['alternateCaptain'],
                            'captain': players_df_full['captain'],
                            'rosterStatus': players_df_full['rosterStatus'],
                            'currentTeam.id': players_df_full['currentTeam.id'],
                            'primaryPosition.name': players_df_full['primaryPosition.name']  }
#         players_df = pd.DataFrame.from_dict(player_part_dict, orient='index')
#     return players_df
    return player_part_dict

def get_player_stats (id):
    url = base_URL + '/people/' + str(id) + '/stats?stats=statsSingleSeason&season=20202021'
    r = requests.get(url)
    if r.status_code != 200:
        print (f"status code is {r.status_code}")
    else:
        data = r.json()
        players_df = pd.json_normalize(data, ['stats'], errors='ignore')
        if players_df['splits'][0] != []:
#             player_info_df = get_player_info (id)
            player_info_dict = get_player_info (id)
            print (player_info_dict)
#             if player_info_dict['primaryPosition.name'] == 'goalie':
            temp= players_df['splits'][0][0]['stat']

            temp_df = pd.DataFrame.from_dict(temp, orient='index')
            temp2_df = temp_df.transpose()
            
            player_part_dict = {'assists': temp2_df['assists'],
                                'goals': temp2_df['goals'],
                                'pim': temp2_df['pim'],
                                'shots': temp2_df['shots'],
                                'games': temp2_df['games'],
                                'powerPlayGoals': temp2_df['powerPlayGoals'],
                                'powerPlayPoints': temp2_df['powerPlayPoints'],
                                'penaltyMinutes': temp2_df['penaltyMinutes'],
                                'plusMinus': temp2_df['plusMinus'],
                                'points': temp2_df['points'] }

            temp3_df = pd.DataFrame.from_dict(player_part_dict, orient='index')

    player_details = pd.concat([player_info_df, temp3_df], axis=1)
    return player_details
        
team_ids = get_teams(); print (f'Got the team ids for {len(team_ids)} teams')
roster_ids = get_rosters (team_ids); print (f'Got the team roster ids for {len(roster_ids)} players')

player_stats =[]
for i, r in enumerate(roster_ids):
    print (i)
    player_stats.append(get_player_stats (r))
    if i == 20:
#         print (player_stats)
        all_players = pd.DataFrame(player_stats)
        make_web ('players', all_players)