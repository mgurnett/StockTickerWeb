from django.shortcuts import render

from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
from pretty_html_table import build_table

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 400
base_URL = "https://statsapi.web.nhl.com/api/v1/"

teams = []; games = []
        
# Create your views here.
def home (request):
    return render (request, 'home.html', {})

#================================
class Team:
    def __init__ (self, id):
        self.id = id
        self.name = ""
        self.teamName = ""
        self.abbreviation = ""
        self.division = ""
        self.conference = ""
        self.venue = ""
        self.win = 0
        self.loss = 0
        self.otloss = 0
        self.soloss = 0
        self.points = 0
        self.game_played = 0
        
    @staticmethod
    def standings (div):
        columns = ['Team', 'Games Played', 'Win', 'Loss', 'OT Loss', 'SO Loss', 'Points', 'Division']
        dummy = [['', 0, 0, 0, 0, 0, 0, '']]
        df = pd.DataFrame(columns=columns, data=dummy)
        for team in teams:
            if team.name:  #see if the team is empty
                team.game_points()
                data = (team.name, team.game_played,
                        team.win, team.loss,
                        team.otloss, team.soloss,
                        team.points, team.division)
                a_series = pd.Series(data, index = df.columns)
                df = df.append(a_series, ignore_index=True)
        df = df.drop(0)
        
        if div == 'all':
            df = df.sort_values(by = 'Points', ascending = False)
        elif div in {'Scotia North', 'Honda West', 'Discover Central', 'MassMutual East'}:
            df = df [df['Division'] == div].sort_values(by = 'Points', ascending = False)
            
        max_gp = df['Games Played'].max()
        df ['GP_adjust'] = round((max_gp / df['Games Played'] * df['Points']), 1)
        df = df.sort_values(by = 'GP_adjust', ascending = False)
        return df    
    
    def name_id (self):
        namestring = f"The team is {self.name} with id of {self.id}"
        return namestring
        
    def crazyname (self):
        print (f"The {self.name} or {self.teamName} of the {self.division} Division of the")
        print (f"{self.conference} Conference play in the {self.venue}")
        
    def game_points (self):
        self.points = self.win * 2 + self.otloss + self.soloss
        self.game_played = self.win + self.otloss + self.soloss + self.loss
        
        
class Game:
    def __init__ (self, id, home_obj, away_obj, date):
        self.id = id
        self.date = date
        self.home_obj = home_obj
        self.away_obj = away_obj
        self.home_score = 0
        self.away_score = 0
        self.game_end = ""
        
    def game_info(self):
        date = self.date.strftime("%a, %b %d, %y")
        game_string = f"{self.home_obj.name} played at home to the {self.away_obj.name} on {date}.  The game ended {self.home_score} - {self.away_score} {self.game_end}"
        return game_string
        
    def point_info(self):
        point_string = f"{self.home_obj.name} has {self.home_obj.points} and {self.away_obj.name} has {self.away_obj.points}"
        return point_string
    
    def games_recorded (self):
        if self.home_score > self.away_score:
            self.home_obj.win += 1
            if self.game_end == "OT":
                self.away_obj.otloss += 1
            elif self.game_end == "SO":
                self.away_obj.soloss += 1
            else:
                self.away_obj.loss += 1
        if self.home_score < self.away_score:
            self.away_obj.win += 1
            if self.game_end == "OT":
                self.home_obj.otloss += 1
            elif self.game_end == "SO":
                self.home_obj.soloss += 1
            else:
                self.home_obj.loss += 1

               
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

    # =======load the games into the Class Games===============
    for i in range(1,max_game_ID):
        url='game/' + year + season_type +str(i).zfill(4) + '/linescore'
        gameID = int(year + season_type +str(i).zfill(4)); #print (gameID)
        data = read_API (url)
        if data['currentPeriod'] != 0:
            home_id = (data['teams']['home']['team']['id'])
            away_id = (data['teams']['away']['team']['id'])
            date_data = data['periods'][0]['startTime']
            datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
            games.append ( Game (gameID, teams[team_manager (home_id)], teams[team_manager (away_id)], datetime_object))
            index = len(games)
            games[index-1].home_score = data['teams']['home']['goals']
            games[index-1].away_score = data['teams']['away']['goals']
            games[index-1].game_end = data['currentPeriodOrdinal']
            games[index-1].games_recorded()

    divis_north = 'Scotia North'
    game_frame_north = Team.standings(divis_north)
    html_name_north = (f'<h1>{divis_north}</h1>')
    html_table_blue_north = build_table(game_frame_north, 'blue_dark')

    divis_central = 'Discover Central'
    game_frame_central = Team.standings(divis_central)
    html_name_central = (f'<h1>{divis_central}</h1>')
    html_table_blue_central = build_table(game_frame_central, 'blue_dark')

    divis_east = 'MassMutual East'
    game_frame_east = Team.standings(divis_east)
    html_name_east = (f'<h1>{divis_east}</h1>')
    html_table_blue_east = build_table(game_frame_east, 'blue_dark')

    divis_west = 'Honda West'
    game_frame_west = Team.standings(divis_west)
    html_name_west = (f'<h1>{divis_west}</h1>')
    html_table_blue_west = build_table(game_frame_west, 'blue_dark')

    divis_NHL = 'NHL'
    game_frame_NHL = Team.standings('all')
    html_name_NHL = (f'<h1>{divis_NHL}</h1>')
    html_table_blue_NHL = build_table(game_frame_NHL, 'blue_dark')
    
    return render (request, 'teams.html', {'tableN': html_table_blue_north, 'nameN': html_name_north,
                                           'tableC': html_table_blue_central, 'nameC': html_name_central,
                                           'tableE': html_table_blue_east, 'nameE': html_name_east,
                                           'tableW': html_table_blue_west, 'nameW': html_name_west,
                                           'tableL': html_table_blue_NHL, 'nameL': html_name_NHL})
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
    team_ids = get_teams(); print (f'Got the team ids for {len(team_ids)} teams')
    roster_ids = get_rosters (team_ids); print (f'Got the team roster ids for {len(roster_ids)} players')

    all_players_df = pd.DataFrame(columns=['id', 'firstName', 'lastName', 'primaryNumber',
                                           'currentAge', 'nationality', 'alternateCaptain',
                                           'captain', 'rosterStatus', 'currentTeam',
                                           'primaryPosition_name', 'points', 'goals', 'assists', 'pim',
                                           'shots', 'games', 'powerPlayGoals', 'powerPlayPoints',
                                           'penaltyMinutes', 'plusMinus'])
    for i, r in enumerate(roster_ids):
        print (i)
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
