from django.shortcuts import render

from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pretty_html_table import build_table
from NHL_classes import *
from div_record import *

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 600
base_URL = "https://statsapi.web.nhl.com/api/v1/"
      
# Create your views here.
def home (request):
    return render (request, 'home.html', {})
               
def read_API (section):
    url = base_URL + section
#     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        return print (f"status code is {r.status_code}")
    else:
        data = r.json()
        return data

def team_manager (team_id):
    global teams
    index = 0
    for i, t in enumerate(teams):
        if t.id == team_id:
            index = i
    if index == 0:
        teams.append (Team (team_id))
        index = len(teams)-1
    return (index)

def teams_view (request):
    teams.append (Team (0))
    # =======load the teams into the Class Teams===============
    df_teams = read_API ("teams")
    dict_teams = df_teams['teams']
    for row in dict_teams:
        id = row['id']
        home_id = team_manager (id)
        teams [home_id].name = row['name']
        teams [home_id].teamName = row['teamName']
        teams [home_id].division = row['division']['name']
        teams [home_id].conference = row['conference']['name']
        teams [home_id].venue = row['venue']['name']
        teams [home_id].abbreviation = row['abbreviation']
    #     teams [home_id].crazyname()

    # print (teams[team_manager (22)].name_id())
    game_box = []
    # =======load the games into the Class Games===============
    for i in range(1,max_game_ID):
        url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
        gameID = int(year + season_type +str(i).zfill(4)); #print (gameID)
        data = read_API (url)
        if data['currentPeriod'] != 0:
            home_id = (data['teams']['home']['team']['id'])
            away_id = (data['teams']['away']['team']['id'])
            date_data = data['periods'][0]['startTime']; print (date_data)
            datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ'); print (datetime_object)
            games.append ( Game (gameID, teams[team_manager (home_id)], teams[team_manager (away_id)], datetime_object))
            index = len(games)-1
            games[index].home_score = data['teams']['home']['goals']
            games[index].away_score = data['teams']['away']['goals']
            games[index].game_end = data['currentPeriodOrdinal']
            games[index].games_recorded()
            curr_game = games[index].game_dict()
#             print (curr_game)
            game_box.append(curr_game)

    all_games_df = pd.DataFrame (game_box)
    all_games_df_date = all_games_df.sort_values('date')
    # all_games_df_date.to_csv (r'all_games.csv', header=True)
    
    div_name = 'Scotia North'
    game_frame_north = Team.standings(div_name)
    html_name_north = (f'<h1>{div_name}</h1>')
    html_table_blue_north = build_table(game_frame_north, 'blue_dark')
    Div_Cube = Cube (div_name, all_games_df_date)
    cube_df = Div_Cube.make_cube()
    div_table_blue_north = build_table(cube_df, 'blue_dark')

    div_name = 'Discover Central'
    game_frame_central = Team.standings(div_name)
    html_name_central = (f'<h1>{div_name}</h1>')
    html_table_blue_central = build_table(game_frame_central, 'blue_dark')
    Div_Cube = Cube (div_name, all_games_df_date)
    cube_df = Div_Cube.make_cube()
    div_table_blue_central = build_table(cube_df, 'blue_dark')

    div_name = 'MassMutual East'
    game_frame_east = Team.standings(div_name)
    html_name_east = (f'<h1>{div_name}</h1>')
    html_table_blue_east = build_table(game_frame_east, 'blue_dark')
    Div_Cube = Cube (div_name, all_games_df_date)
    cube_df = Div_Cube.make_cube()
    div_table_blue_east = build_table(cube_df, 'blue_dark')

    div_name = 'Honda West'
    game_frame_west = Team.standings(div_name)
    html_name_west = (f'<h1>{div_name}</h1>')
    html_table_blue_west = build_table(game_frame_west, 'blue_dark')
    Div_Cube = Cube (div_name, all_games_df_date)
    cube_df = Div_Cube.make_cube()
    div_table_blue_west = build_table(cube_df, 'blue_dark')

    div_name = 'NHL'
    game_frame_NHL = Team.standings('all')
    html_name_NHL = (f'<h1>{div_name}</h1>')
    html_table_blue_NHL = build_table(game_frame_NHL, 'blue_dark')
    
    html_name_debug = (f'<h1>All Games</h1>')
    html_table_blue_debug = build_table(all_games_df_date, 'blue_dark')

    return render (request, 'teams.html', {'tableN': html_table_blue_north, 'nameN': html_name_north, 
                                            'divtableN': div_table_blue_north,
                                           'tableC': html_table_blue_central, 'nameC': html_name_central,
                                            'divtableC': div_table_blue_central,
                                           'tableE': html_table_blue_east, 'nameE': html_name_east,
                                            'divtableE': div_table_blue_east,
                                           'tableW': html_table_blue_west, 'nameW': html_name_west,
                                            'divtableW': div_table_blue_west,
                                           'tableL': html_table_blue_NHL, 'nameL': html_name_NHL,
                                           'tableDB': html_table_blue_debug, 'nameDB': html_name_debug})
#===========================

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
                             'assists': data_stat.get('assists'),
                             'pim': data_stat.get('pim'),
                             'shots': data_stat.get('shots'),
                             'games': data_stat.get('games'),
                             'powerPlayGoals': data_stat.get('powerPlayGoals'),
                             'powerPlayPoints': data_stat.get('powerPlayPoints'),
                             'penaltyMinutes': data_stat.get('penaltyMinutes'),
                             'plusMinus': data_stat.get('plusMinus')  }
#         print (player_stats_dict)
        url = base_URL + '/people/' + str(id)
        data = get_player_data (url)#; print ('data', type(data), data)
        data_people = data['people'][0]#; print ('data_people', type(data_people), data_people)
#         print (data_people.keys())#; print ('data_splits', type(data_splits), data_splits)
#         player_team_id = data_people.get('currentTeam').get('id'); print ('player_team_id', type(player_team_id), player_team_id)
#         pti = player_team_id.get('id'); print ('pti', type(pti), pti)
        player_info_dict = {'id': data_people.get('id'),
                            'firstName': data_people.get('firstName'),
                            'lastName': data_people.get('lastName'),
                            'primaryNumber': data_people.get('primaryNumber'),
                            'currentAge': data_people.get('currentAge'),
                            'nationality': data_people.get('nationality'),
                            'alternateCaptain': data_people.get('alternateCaptain'),
                            'captain': data_people.get('captain'),
                            'rosterStatus': data_people.get('rosterStatus'),
                            'currentTeam': data_people.get('currentTeam').get('name'),
                            'primaryPosition_name': data_people.get('primaryPosition').get('name')  }
        player_info_dict.update(player_stats_dict)#; print ('player_info_dict', type(player_info_dict), player_info_dict)
#         print (player_info_dict.keys())
        all_players_df = pd.DataFrame(player_info_dict, index=['i',])

    else:
        all_players_df = []
    return all_players_df
        
def build_dataframe ():
    team_ids = get_teams(); #print (f'Got the team ids for {len(team_ids)} teams')
    roster_ids = get_rosters (team_ids); #print (f'Got the team roster ids for {len(roster_ids)} players')

    all_players_df = pd.DataFrame(columns=['id', 'firstName', 'lastName', 'primaryNumber',
                                           'currentAge', 'nationality', 'alternateCaptain',
                                           'captain', 'rosterStatus', 'currentTeam',
                                           'primaryPosition_name', 'points', 'goals', 'assists', 'pim',
                                           'shots', 'games', 'powerPlayGoals', 'powerPlayPoints',
                                           'penaltyMinutes', 'plusMinus'])
    for i, r in enumerate(roster_ids):
        #print (i)
        player_stats_df = (get_player_info (r))#; print ('player_stats_df', type(player_stats_df), player_stats_df)
        all_players_df = all_players_df.append(player_stats_df)#; print ('all_players_df', type(all_players_df), all_players_df)
    return all_players_df

def players_view (request):

    all_players_df = build_dataframe()
    
    scorers_sub = all_players_df.sort_values(by=['goals', 'assists'], ascending=False).head(10)
    scorers = scorers_sub[['firstName', 'lastName', 'currentTeam', 'points', 'goals', 'assists']]
    html_table_scorers = build_table(scorers, 'blue_dark')
    
    defence = all_players_df.groupby(["primaryPosition_name"]).get_group(("Defenseman"))
    d_points = defence.sort_values(by=['points', 'goals'], ascending=False).head(10)
    d_points_sub = d_points[['firstName', 'lastName', 'currentTeam', 'points', 'goals', 'assists']]
    html_table_d_points_sub = build_table(d_points_sub, 'blue_dark')

    points_sub = all_players_df.sort_values(by=['points', 'goals'], ascending=False).head(10)
    points = points_sub[['firstName', 'lastName', 'currentTeam', 'points', 'goals', 'assists']]
    html_table_points = build_table(points, 'blue_dark')

    plusMinus_sub = all_players_df.sort_values(by=['plusMinus'], ascending=False).head(10)
    plusMinus = plusMinus_sub[['firstName', 'lastName', 'currentTeam', 'plusMinus', 'points', 'goals', 'assists']]
    html_table_plusMinus = build_table(plusMinus, 'blue_dark')

    
    return render (request, 'players.html', {'tableS': html_table_scorers,      'nameS': 'Goals',
                                             'tableD': html_table_d_points_sub, 'nameD': 'Defence goals',
                                             'tableP': html_table_points,       'nameP': 'Points',
                                             'tablePM': html_table_plusMinus,   'namePM': 'Plus/minus'})
