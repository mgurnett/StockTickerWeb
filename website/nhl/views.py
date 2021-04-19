from django.shortcuts import render

from datetime import datetime
import pytz
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pretty_html_table import build_table
import pickle
from Team_class import *
from Game_class import *
from div_record import *
from API_read import read_API

# Set up the API call variables
year = '2020'
season_type = '02'
max_game_ID = 600
base_URL = "https://statsapi.web.nhl.com/api/v1/"
# Create your views here.


def home(request):
    return render(request, 'home.html', {})

def team_stats (self):
    for team in self.teams:
        url = (f'teams/{team.id}/stats')
        team_json = read_API (url)
        # packages_str = json.dumps (team_json['stats'][0]['splits'][0]['stat'], indent =2)
        # print (packages_str)
        team.games_played = team_json['stats'][0]['splits'][0]['stat']['gamesPlayed']
        team.win = team_json['stats'][0]['splits'][0]['stat']['wins']
        team.loss = team_json['stats'][0]['splits'][0]['stat']['losses']
        team.otloss = team_json['stats'][0]['splits'][0]['stat']['ot']
        team.points = team_json['stats'][0]['splits'][0]['stat']['pts']
        team.point_percent = team_json['stats'][0]['splits'][0]['stat']['ptPctg']

def load_teams ():
    '''load the teams data from the file if it is there, or get it from the API if it isn't.'''
    leag = []
    try:
        with open(f'teams.pickle', 'rb') as file:
            leag = pickle.load(file)
            print ('loaded teams from the file')
    except IOError:
        packages_json = read_API ('teams')
        team_list = []
        for index in range (len(packages_json['teams'])):
            team_id = packages_json['teams'][index]['id']
            current_team = Team (team_id)
            current_team.name = packages_json['teams'][index]['name']
            current_team.abbreviation = packages_json['teams'][index]['abbreviation']
            current_team.teamName = packages_json['teams'][index]['teamName']
            current_team.locationName = packages_json['teams'][index]['locationName']
            current_team.shortName = packages_json['teams'][index]['shortName']
            current_team.division = packages_json['teams'][index]['division']['name']
            current_team.venue = packages_json['teams'][index]['venue']['name']
            team_list.append (current_team)
            # print (current_team)

        leag = AllTeams (team_list)
        # for team in league.teams:
        #     print (team)

        with open(f'teams.pickle', 'wb') as file:
            pickle.dump(leag, file)
            print ('loaded teams from the API and then saved them to the file')
    return (leag)

def teams_view(request):

    league = load_teams ()
    if league != []:
        for team in league.teams:
            packages_json = read_API ('teams')
        pass
    else:
        print ('FAILURE')
        
    league.team_stats()
    schedule = load_api_games ()
    div_name = 'Scotia North'
    game_frame_north = AllTeams.standings(league.teams, div_name)
    html_name_north = (f'<h1>{div_name}</h1>')
    html_table_blue_north = build_table(
        game_frame_north, 'blue_dark', text_align='centre')
    Div_Cube = Cube(div_name, league, schedule)
    cube_df = Div_Cube.make_cube()
    div_table_blue_north = build_table(cube_df, 'blue_dark')

    div_name = 'Discover Central'
    game_frame_central = AllTeams.standings(league.teams, div_name)
    html_name_central = (f'<h1>{div_name}</h1>')
    html_table_blue_central = build_table(game_frame_central, 'blue_dark')
    Div_Cube = Cube(div_name, league, schedule)
    cube_df = Div_Cube.make_cube()
    div_table_blue_central = build_table(cube_df, 'blue_dark')

    div_name = 'MassMutual East'
    game_frame_east = AllTeams.standings(league.teams, div_name)
    html_name_east = (f'<h1>{div_name}</h1>')
    html_table_blue_east = build_table(game_frame_east, 'blue_dark')
    Div_Cube = Cube(div_name, league, schedule)
    cube_df = Div_Cube.make_cube()
    div_table_blue_east = build_table(cube_df, 'blue_dark')

    div_name = 'Honda West'
    game_frame_west = AllTeams.standings(league.teams, div_name)
    html_name_west = (f'<h1>{div_name}</h1>')
    html_table_blue_west = build_table(game_frame_west, 'blue_dark')
    Div_Cube = Cube(div_name, league, schedule)
    cube_df = Div_Cube.make_cube()
    div_table_blue_west = build_table(cube_df, 'blue_dark')

    div_name = 'NHL'
    game_frame_NHL = AllTeams.standings(league.teams, div_name)
    html_name_NHL = (f'<h1>{div_name}</h1>')
    html_table_blue_NHL = build_table(game_frame_NHL, 'blue_dark')
    
    the_date_yest = datetime.now() -  timedelta(hours=30)#; the_date = the_date.date()
    # debug_var ('the_date', the_date)
    yest_games_df = pd.DataFrame.from_dict(schedule.games_on_a_day(the_date_yest), orient='columns')
    html_name_yest = (f'<h1>Yesterday</h1>')
    html_table_yest_games = build_table(yest_games_df, 'blue_dark')
    
    the_date_today = datetime.now() -  timedelta(hours=6)#; the_date = the_date.date()
    # debug_var ('the_date', the_date)
    today_games_df = pd.DataFrame.from_dict(schedule.games_on_a_day(the_date_today), orient='columns')
    html_name_today = (f'<h1>Today</h1>')
    html_table_today_games = build_table(today_games_df, 'blue_dark')
    
    the_date_tom = datetime.now() +  timedelta(hours=18)#; the_date = the_date.date()
    # debug_var ('the_date', the_date)
    tom_games_df = pd.DataFrame.from_dict(schedule.games_on_a_day(the_date_tom), orient='columns')
    html_name_tom = (f'<h1>Tomorrow</h1>')
    html_table_tom_games = build_table(tom_games_df, 'blue_dark')
    
    return render(request, 'teams.html', {'tableN': html_table_blue_north, 'nameN': html_name_north, 'divtableN': div_table_blue_north,
                                          'tableC': html_table_blue_central, 'nameC': html_name_central, 'divtableC': div_table_blue_central,
                                          'tableE': html_table_blue_east, 'nameE': html_name_east, 'divtableE': div_table_blue_east,
                                          'tableW': html_table_blue_west, 'nameW': html_name_west, 'divtableW': div_table_blue_west,
                                          'tableL': html_table_blue_NHL, 'nameL': html_name_NHL,
                                          'yest_games': html_table_yest_games, 'nameyest': html_name_yest, 'yest_date': the_date_yest.date,
                                          'today_games': html_table_today_games, 'nametoday': html_name_today, 'today_date': the_date_today.date,
                                          'tom_games': html_table_tom_games, 'nametom': html_name_tom, 'tom_date': the_date_tom.date
                                            })
                                            
                                        #   'tableDB': html_table_blue_debug, 'nameDB': html_name_debug})
# ===========================


def get_teams():
    team_id = []
    url = base_URL + 'teams'
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print(f"status code is {r.status_code}")
    else:
        data = r.json()
        teams_df = pd.json_normalize(data, ['teams'], errors='ignore')
        team_id = teams_df['id']
    #     print (team_id)
    #     make_web ('teams', teams_df)
    return team_id


def get_rosters(t_id):
    roster = []
    active_roster = []
    for team in t_id:
        url = base_URL + '/teams/' + str(team) + '/roster'
    #     print (url)
        r = requests.get(url)
        if r.status_code != 200:
            print(f"status code is {r.status_code}")
        else:
            data = r.json()
            roster_df = pd.json_normalize(data, ['roster'],  errors='ignore')
            # ; print (roster_df['person.id'])
            roster.append(roster_df['person.id'])
            for r in roster_df['person.id']:
                active_roster.append(r)
    return active_roster


def get_player_data(url):
    #     print (url)
    r = requests.get(url)
    if r.status_code != 200:
        print(f"status code is {r.status_code}")
    else:
        data = r.json()
    return data


def get_player_info(id):
    # Player stats
    url = base_URL + '/people/' + \
        str(id) + '/stats?stats=statsSingleSeason&season=20202021'
    data = get_player_data(url)  # data is a <class 'dict'>
    # ; print ('data_stats', type(data_stats), data_stats)
    data_stats = data['stats'][0]
    # ; print ('data_splits', type(data_splits), data_splits)
    data_splits = data_stats['splits']

    if data_splits != []:
        # ; print ('data_splits', type(data_splits), data_splits)
        data_splits = data_stats['splits'][0]
        # ; print ('data_stat', type(data_stat), data_stat.keys())
        data_stat = data_splits['stat']
        player_stats_dict = {'points': data_stat.get('points'),
                             'goals': data_stat.get('goals'),
                             'assists': data_stat.get('assists'),
                             'pim': data_stat.get('pim'),
                             'shots': data_stat.get('shots'),
                             'games': data_stat.get('games'),
                             'powerPlayGoals': data_stat.get('powerPlayGoals'),
                             'powerPlayPoints': data_stat.get('powerPlayPoints'),
                             'penaltyMinutes': data_stat.get('penaltyMinutes'),
                             'plusMinus': data_stat.get('plusMinus')}
#         print (player_stats_dict)
        url = base_URL + '/people/' + str(id)
        data = get_player_data(url)  # ; print ('data', type(data), data)
        # ; print ('data_people', type(data_people), data_people)
        data_people = data['people'][0]
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
                            'primaryPosition_name': data_people.get('primaryPosition').get('name')}
        # ; print ('player_info_dict', type(player_info_dict), player_info_dict)
        player_info_dict.update(player_stats_dict)
#         print (player_info_dict.keys())
        all_players_df = pd.DataFrame(player_info_dict, index=['i', ])

    else:
        all_players_df = []
    return all_players_df


def build_dataframe():
    # print (f'Got the team ids for {len(team_ids)} teams')
    team_ids = get_teams()
    # print (f'Got the team roster ids for {len(roster_ids)} players')
    roster_ids = get_rosters(team_ids)

    all_players_df = pd.DataFrame(columns=['id', 'firstName', 'lastName', 'primaryNumber',
                                           'currentAge', 'nationality', 'alternateCaptain',
                                           'captain', 'rosterStatus', 'currentTeam',
                                           'primaryPosition_name', 'points', 'goals', 'assists', 'pim',
                                           'shots', 'games', 'powerPlayGoals', 'powerPlayPoints',
                                           'penaltyMinutes', 'plusMinus'])
    for i, r in enumerate(roster_ids):
        #print (i)
        # ; print ('player_stats_df', type(player_stats_df), player_stats_df)
        player_stats_df = (get_player_info(r))
        # ; print ('all_players_df', type(all_players_df), all_players_df)
        all_players_df = all_players_df.append(player_stats_df)
    return all_players_df


def players_view(request):

    all_players_df = build_dataframe()

    scorers_sub = all_players_df.sort_values(
        by=['goals', 'assists'], ascending=False).head(10)
    scorers = scorers_sub[['firstName', 'lastName',
                           'currentTeam', 'points', 'goals', 'assists']]
    html_table_scorers = build_table(scorers, 'blue_dark')

    defence = all_players_df.groupby(
        ["primaryPosition_name"]).get_group(("Defenseman"))
    d_points = defence.sort_values(
        by=['points', 'goals'], ascending=False).head(10)
    d_points_sub = d_points[['firstName', 'lastName',
                             'currentTeam', 'points', 'goals', 'assists']]
    html_table_d_points_sub = build_table(d_points_sub, 'blue_dark')

    points_sub = all_players_df.sort_values(
        by=['points', 'goals'], ascending=False).head(10)
    points = points_sub[['firstName', 'lastName',
                         'currentTeam', 'points', 'goals', 'assists']]
    html_table_points = build_table(points, 'blue_dark')

    plusMinus_sub = all_players_df.sort_values(
        by=['plusMinus'], ascending=False).head(10)
    plusMinus = plusMinus_sub[['firstName', 'lastName',
                               'currentTeam', 'plusMinus', 'points', 'goals', 'assists']]
    html_table_plusMinus = build_table(plusMinus, 'blue_dark')

    return render(request, 'players.html', {'tableS': html_table_scorers,      'nameS': 'Goals',
                                            'tableD': html_table_d_points_sub, 'nameD': 'Defence goals',
                                            'tableP': html_table_points,       'nameP': 'Points',
                                            'tablePM': html_table_plusMinus,   'namePM': 'Plus/minus'})