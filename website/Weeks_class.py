from datetime import datetime, timedelta
from Game_class import *

class Weeks:
    def __init__(self, schedule):
        self.todays_date = datetime.now()
        self.last_week_start = self.todays_date - timedelta(days=7)
        self.last_week_end = self.todays_date - timedelta(days=2)
        self.yesterday = self.todays_date - timedelta(days=1)
        self.tomorrow =  self.todays_date + timedelta(days=1)
        self.next_week_start = self.todays_date + timedelta(days=2)
        self.next_week_end = self.todays_date + timedelta(days=7)

        self.yesterday_table = schedule.games_on_a_day(self.yesterday) #is type dict
        self.today_table = schedule.games_on_a_day(self.todays_date) #is type dict
        self.tomorrow_table = schedule.games_on_a_day(self.tomorrow) #is type dict
        self.last_week_table = self.last_week_table_make()

    def last_week_table_make (self):
        self.last_week_table = []
        for d in range(7, 1):
            self.last_week_table.append(schedule.games_on_a_day(self.todays_date - timedelta(days=7)))

schedule = load_api_games ()
two_weeks = Weeks(schedule)
print (two_weeks.last_week_table)