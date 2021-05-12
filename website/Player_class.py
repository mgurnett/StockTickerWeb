import pickle
import json
import requests
import pandas as pd
from API_read import read_API
from Team_class import *

base_URL = "https://statsapi.web.nhl.com/api/v1/"

class Player:
    ''' The Player class for a player '''
    def __init__ (self, id):
        self.id = id
        self.first_name = ''
        self.lastName = ''
        self.primaryNumber = ''
        self.currentAge = ''
        self.nationality = ''
        self.alternateCaptain = ''
        self.captain = ''
        self.rosterStatus = ''
        self.currentTeam = ''
        self.primaryPosition_name = ''
        self.birthDate = ''
        self.birthCountry = ''
        self.nationality = ''
        self.rookie = ''
        self.shootsCatches = ''
        self.load_player_data()

    def __str__ (self):
        return (f'{self.first_name} {self.lastName} (#{self.primaryNumber}) {self.primaryPosition_name} Active:{self.rosterStatus} & is {self.currentAge} years old')

    def load_player_data (self):
        url = (f'people/{str(self.id)}')
        data = read_API (url)
        data_people = data['people'][0]
        self.first_name = data_people.get('firstName')
        self.lastName = data_people.get('lastName')
        self.primaryNumber = data_people.get('primaryNumber')
        self.currentAge = data_people.get('currentAge')
        self.nationality = data_people.get('nationality')
        self.alternateCaptain = data_people.get('alternateCaptain')
        self.captain = data_people.get('captain')
        self.rosterStatus = data_people.get('rosterStatus')
        self.currentTeam = data_people.get('currentTeam').get('name')
        self.primaryPosition_name = data_people.get('primaryPosition').get('name')
        self.birthDate = data_people.get('birthDate')
        self.birthCountry = data_people.get('birthCountry')
        self.nationality = data_people.get('nationality')
        self.rookie = data_people.get('rookie')
        self.shootsCatches = data_people.get('shootsCatches')

class Skater (Player):
    #https://statsapi.web.nhl.com/api/v1/people/8478402 McDavid
    def __init__(self, id):
        super.__init__(self, id)
        self.timeOnIce = ''
        self.assists = ''
        self.goals = ''
        self.pim = ''
        self.shots = ''
        self.games = ''
        self.hits = ''
        self.powerPlayGoals = ''
        self.powerPlayPoints = ''
        self.powerPlayTimeOnIce = ''
        self.evenTimeOnIce = ''
        self.penaltyMinutes = ''
        self.faceOffPct = ''
        self.shotPct = ''
        self.gameWinningGoals = ''
        self.overTimeGoals = ''
        self.shortHandedGoals = ''
        self.shortHandedPoints = ''
        self.shortHandedTimeOnIce = ''
        self.blocked = ''
        self.plusMinus = ''
        self.points = ''
        self.shifts = ''
        self.timeOnIcePerGame = ''
        self.evenTimeOnIcePerGame = ''
        self.shortHandedTimeOnIcePerGame = ''
        self.powerPlayTimeOnIcePerGame = ''
        self.load_skater_data()

    def __str__ (self):
        return (f'{self.first_name} {self.lastName} (#{self.primaryNumber}) {self.primaryPosition_name} and has {self.points} points.')

    def load_skater_data (self):
        url = (f'people/{str(self.id)}/stats?stats=statsSingleSeason&season=20202021')
        data = read_API (url)
        data_stats = data['stats'][0]
        data_splits = data_stats['splits']
        self.timeOnIce = data_people.get('timeOnIce')
        self.assists = data_people.get('assists')
        self.goals = data_people.get('goals')
        self.pim = data_people.get('pim')
        self.shots = data_people.get('shots')
        self.games = data_people.get('games')
        self.hits = data_people.get('hits')
        self.powerPlayGoals = data_people.get('powerPlayGoals')
        self.powerPlayPoints = data_people.get('powerPlayPoints')
        self.powerPlayTimeOnIce = data_people.get('powerPlayTimeOnIce')
        self.evenTimeOnIce = data_people.get('evenTimeOnIce')
        self.penaltyMinutes = data_people.get('penaltyMinutes')
        self.faceOffPct = data_people.get('faceOffPct')
        self.shotPct = data_people.get('shotPct')
        self.gameWinningGoals = data_people.get('gameWinningGoals')
        self.overTimeGoals = data_people.get('overTimeGoals')
        self.shortHandedGoals = data_people.get('shortHandedGoals')
        self.shortHandedPoints = data_people.get('shortHandedPoints')
        self.shortHandedTimeOnIce = data_people.get('shortHandedTimeOnIce')
        self.blocked = data_people.get('blocked')
        self.plusMinus = data_people.get('plusMinus')
        self.points = data_people.get('points')
        self.shifts = data_people.get('shifts')
        self.timeOnIcePerGame = data_people.get('timeOnIcePerGame')
        self.evenTimeOnIcePerGame = data_people.get('evenTimeOnIcePerGame')
        self.shortHandedTimeOnIcePerGame = data_people.get('shortHandedTimeOnIcePerGame')
        self.powerPlayTimeOnIcePerGame = data_people.get('powerPlayTimeOnIcePerGame')


class Goalie (Player):
    #https://statsapi.web.nhl.com/api/v1/people/8469608 Mike Smith
    def __init__(self, id):
        super.__init__(self, id)
        self.timeOnIce = ''
        self.ot = ''
        self.shutouts = ''
        self.ties = ''
        self.wins = ''
        self.losses = ''
        self.saves = ''
        self.powerPlaySaves = ''
        self.shortHandedSaves = ''
        self.evenSaves = ''
        self.shortHandedShots = ''
        self.evenShots = ''
        self.powerPlayShots = ''
        self.savePercentage = ''
        self.goalAgainstAverage = ''
        self.games = ''
        self.gamesStarted = ''
        self.shotsAgainst = ''
        self.goalsAgainst = ''
        self.timeOnIcePerGame = '',
        self.powerPlaySavePercentage = ''
        self.shortHandedSavePercentage = ''
        self.evenStrengthSavePercentage = ''
        self.load_goalie_data()

    def __str__ (self):
        return (f'{self.first_name} {self.lastName} (#{self.primaryNumber}) {self.primaryPosition_name} and has {self.wins} wins.')

    def load_goalie_data (self):
        url = (f'people/{str(self.id)}/stats?stats=statsSingleSeason&season=20202021')
        data = read_API (url)
        data_stats = data['stats'][0]
        data_splits = data_stats['splits']
        self.timeOnIce = data_people.get('timeOnIce')
        self.ot = data_people.get('ot')
        self.shutouts = data_people.get('shutouts')
        self.ties = data_people.get('ties')
        self.wins = data_people.get('wins')
        self.losses = data_people.get('losses')
        self.saves = data_people.get('saves')
        self.powerPlaySaves = data_people.get('powerPlaySaves')
        self.shortHandedSaves = data_people.get('shortHandedSaves')
        self.evenSaves = data_people.get('evenSaves')
        self.shortHandedShots = data_people.get('shortHandedShots')
        self.evenShots = data_people.get('evenShots')
        self.powerPlayShots = data_people.get('powerPlayShots')
        self.savePercentage = data_people.get('savePercentage')
        self.goalAgainstAverage = data_people.get('goalAgainstAverage')
        self.games = data_people.get('games')
        self.gamesStarted = data_people.get('gamesStarted')
        self.shotsAgainst = data_people.get('shotsAgainst')
        self.goalsAgainst = data_people.get('goalsAgainst')
        self.timeOnIcePerGame = data_people.get('timeOnIcePerGame'),
        self.powerPlaySavePercentage = data_people.get('powerPlaySavePercentage')
        self.shortHandedSavePercentage = data_people.get('shortHandedSavePercentage')
        self.evenStrengthSavePercentage = data_people.get('evenStrengthSavePercentage')

'''
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
'''

if __name__ == '__main__':
    league = load_teams ()
    league.team_stats()
    # for cur_team in league.teams:
    #     print (cur_team)

    current_team = league.teams [20]
    print (current_team)
    # print (current_team.print_roster())
    full_roster = current_team.roster
    for player_id in full_roster:
        current_player = Player (player_id)
        print (current_player)
