from API_read import read_API
from datetime import datetime
import pytz

year = '2020'
season_type = '02'

class Game:
    def __init__ (self, id):
        self.id = id
        self.status = ''
        self.date = ''
        self.home = ''
        self.away = ''
        self.home_score = 0
        self.away_score = 0
        self.home_point = 0
        self.away_point = 0

    def __str__ (self):
        if self.status == 'Final':
            return (f'{self.date} ({self.id}) {self.home} was home to the {self.away}.  The score was {self.home_score} - {self.away_score} {self.status}')
        elif self.status in ('In Progress', 'Pre-Game'):
            return (f'{self.date} ({self.id}) {self.home} is home to the {self.away}.  The score is {self.home_score} - {self.away_score} {self.status}')
        else:
            return (f'{self.date} ({self.id}) {self.home} will be home to the {self.away}.  {self.status}')

    def live_games (self):
        if self.status in ('In Progress', 'Pre-Game'):
            return (f'{self.date} ({self.id}) {self.home} is home to the {self.away}.  The score is {self.home_score} - {self.away_score} {self.status}')

class AllGames:
    def __init__ (self, GameObjects):
        self.games = list(GameObjects)

    def __str__ (self):
        schedule_status = {'Final': 0, 'Postponed': 0, 'Scheduled': 0, 'Pre-Game': 0, 'total':0}
        for x in self.games:
            if x.status == 'Final':
                schedule_status['Final'] += 1
            elif x.status == 'Postponed':
                schedule_status['Postponed'] += 1
            elif x.status == 'Scheduled':
                schedule_status['Scheduled'] += 1
            elif x.status == 'Pre-Game':
                schedule_status['Pre-Game'] += 1
            else:
                print (x.status)
            schedule_status['total'] += 1

        return (f"There are {schedule_status['Final']} finished games in a schedule of {schedule_status['total']} games {schedule_status}")

    def types_of_games (self):
        types = []
        for game in self.games:
            game_type = game.status
            if game_type in types:
                pass
            else:
                types.append (game_type)
        return types

def load_api_games ():
    '''get all games from API'''
    schedule = []
    url = 'schedule?startDate=2021-01-01&endDate=2021-07-01'
    data = read_API(url)
    for api_dates in data['dates']:
        for api_games in api_dates['games']:
            current_game = Game (api_games['gamePk'])
            current_game.date = fix_time(api_games['gameDate'])
            current_game.home = api_games['teams']['home']['team']['name']
            current_game.away = api_games['teams']['away']['team']['name']
            current_game.status = api_games['status']['detailedState']
            if current_game.status in ['Final','In Progress']:
                current_game.home_score = api_games['teams']['home']['score']
                current_game.away_score = api_games['teams']['away']['score']
            if current_game.status in ['Final']:

                current_game.home_point = api_games['teams']['home']['score']
                current_game.away_point = api_games['teams']['away']['score']
            schedule.append (current_game)
            # print (current_game)

    sche = AllGames (schedule)
    return (sche)

def fix_time (api_dt): 
    # print (f'api_dt {api_dt} of {type(api_dt)}')
    datetime_object = datetime.strptime(api_dt, '%Y-%m-%dT%H:%M:%SZ')
    UTC_time = pytz.timezone("UTC").localize(datetime_object)
    d = UTC_time.astimezone()
    Edmonton_time = d.strftime("%d %b %Y (%I:%M %p) %Z") #Print it with a directive of choice
    # Edmonton_time = d.strftime("%Y-%m-%dT%H:%M:%SZ") #Print it with a directive of choice
    return (Edmonton_time)

if __name__ == '__main__':
    schedule = load_api_games ()
    if schedule != []:
        for game in schedule.games:
            if game.status in  ('In Progress', 'Pre-Game'):
                print (game.live_games())
        print (schedule)
        pass
    else:
        print ('FAILURE')