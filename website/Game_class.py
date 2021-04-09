from API_read import read_API
from datetime import datetime
import pytz

year = '2020'
season_type = '02'
local_tz = pytz.timezone('America/Edmonton')

class Game:
    def __init__ (self, id):
        self.id = id
        self.status = ''
        self.date = ''
        self.home = ''
        self.away = ''
        self.home_object = ''
        self.away_object = ''
        self.home_score = 0
        self.away_score = 0
        self.home_point = 0
        self.away_point = 0

    def __str__ (self):
        if self.status == 'Final':
            return (f'{self.date} ({self.id}) {self.home} was home to the {self.away}.  The score was {self.home_score} - {self.away_score} {self.status}')
        elif self.status in ('In Progress', 'Pre-Game'):
            return (f'{self.date} ({self.id}) {self.home} are home to the {self.away}.  The score is {self.home_score} - {self.away_score} {self.status}')
        else:
            return (f'{self.date} ({self.id}) {self.home} will be home to the {self.away}.  {self.status}')

class AllGames:
    def __init__ (self, GameObjects):
        self.games = list(GameObjects)

    @staticmethod
    def fix_time (api_dt): #api_dt is <class 'str'>
        print (f"api_dt is {api_dt} of type {type(api_dt)}")
        # print (f"current time is {datetime.now()}  with timezone of {datetime.now().tzinfo} of type {type(datetime.now())}")

        # datetime_object = datetime.strptime(api_dt, '%Y-%m-%dT%H:%M:%SZ') # datetime_object is <class 'datetime.datetime'>
    #     print (f"datetime_object is {datetime_object} with timezone of {datetime_object.tzinfo} of type {type(datetime_object)}")
    #     # time is now an object with NO timezone
       
    #     UTC_time = pytz.timezone("UTC").localize(datetime_object)  #UTC_time is <class 'datetime.datetime'> WITH A UTC timezone
    #     print (f"UTC_time is {UTC_time} of type {type(UTC_time)}")
        
    #     d = UTC_time.astimezone() #d is <class 'datetime.datetime'>
    #     print (f"d is {d} of type {type(d)}")
        
    #     Edmonton_time = d.strftime("%Y-%m-%dT%H:%M:%SZ") # Edmonton_time is <class 'str'>  - NOT USED Can be done locally
    #     # print (f"d is {d.date()} and the time is {d.time()} in the timezone of {d.tzinfo}")
    #     print (f"time IN {UTC_time.date()}-{UTC_time.time()} ({UTC_time.tzinfo}) and time OUT {d.date()}-{d.time()} ({d.tzinfo})")
    #     return (d) # d is <class 'datetime.datetime'> 2021-05-11 and the time is 17:00:00 in the timezone of MDT

        local_dt = api_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)

    def __str__ (self):
        schedule_status = {'Final': 0, 'Postponed': 0, 'Scheduled': 0, 'Pre-Game': 0, 'In Progress':0, 'total':0}
        for x in self.games:
            if x.status == 'Final':
                schedule_status['Final'] += 1
            elif x.status == 'Postponed':
                schedule_status['Postponed'] += 1
            elif x.status == 'Scheduled':
                schedule_status['Scheduled'] += 1
            elif x.status == 'Pre-Game':
                schedule_status['Pre-Game'] += 1
            elif x.status == 'In Progress':
                schedule_status['In Progress'] += 1
            else:
                print (x.status)
            schedule_status['total'] += 1

        return (f"There are {schedule_status['Final']} finished games in a schedule of {schedule_status['total']} games \n {schedule_status}")

    def types_of_games (self):
        types = []
        for game in self.games:
            game_type = game.status
            if game_type in types:
                pass
            else:
                types.append (game_type)
        return types

    def games_on_a_day (self, targ_date=datetime.now()):
        games_otd = []
        # print (f'Today is {targ_date.date()} and the time is {targ_date.time()} in the timezone of {targ_date.tzinfo}')
        for game in self.games:
            # game_date = game.date.strftime("%Y-%m-%dT%H:%M:%SZ") # game_date is <class 'str'>
            game_date = game.date
            # print (f'The game.date is {type(game_date)} {game_date}')
            if game_date.date() == targ_date.date():
                # print (f'The game_date is {game_date.date()}.  The targ_date is {targ_date.date()} {game}')
                game_dict = {'date': game_date,
                    'home':game.home,
                    'home_score':game.home_score,
                    'away_score':game.away_score,
                    'away':game.away,
                    'status':game.status}
                games_otd.append(game_dict)
        return (games_otd)

def load_api_games ():
    '''get all games from API'''
    schedule = []
    url = 'schedule?startDate=2021-01-01&endDate=2021-07-01'
    data = read_API(url)
    for api_dates in data['dates']:
        for api_games in api_dates['games']:
            current_game = Game (api_games['gamePk'])
            date_object = api_games['gameDate'].strftime("%Y-%m-%dT%H:%M:%SZ")
            current_game.date = AllGames.fix_time(date_object) # current_game is <class 'datetime.datetime'>
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

if __name__ == '__main__':
    schedule = load_api_games ()
    # if schedule != []:
    #     for game in schedule.games:
    #         game.live_games()
    #         game.today_games()
    #     print (schedule)
        
    # else:
    #     print ('FAILURE')

    # schedule.games_on_a_day()
    # print (schedule)

    # api_dt = '2021-05-11T23:00:00Z'
    # datetime_object = datetime.strptime(api_dt, '%Y-%m-%dT%H:%M:%SZ')
    # print(api_dt)
    # newtime = AllGames.fix_time(datetime_object)
    # print (newtime.tzinfo)