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
        # print (data_people)

        # url = (f'people/{str(self.id)}/stats?stats=statsSingleSeason&season=20202021')
        # player_json = read_API (url)
        # data_stats = player_json['stats'][0]
        # data_splits = data_stats['splits']

        # if data_splits != []:
        #     # ; print ('data_splits', type(data_splits), data_splits)
        #     data_splits = data_stats['splits'][0]
        #     # ; print ('data_stat', type(data_stat), data_stat.keys())
        #     data_stat = data_splits['stat']
        #     print (data_stat)


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
