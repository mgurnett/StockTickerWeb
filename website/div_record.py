import pandas as pd
from makeweb import make_web
from pretty_html_table import build_table
from Team_class import *
from Game_class import *

class Cube:
    def __init__ (self, division, league, schedule):
        '''send the division name, teams and leagues classes'''
        self.division = division
        self.schedule = schedule
        self.league = league
        self.games_list_df = self.get_games()
        self.teams_list = self.get_teams()
        self.cube = pd.DataFrame ({'tt': 0, 'lt': 0},columns=self.teams_list, index=self.teams_list)

    def __str__ (self):
        return (f'{self.cube}')

    def get_games (self):
        games_list = []
        div_list = []
        for t in self.league.teams:
            if t.division == self.division:
                div_list.append (t.name)
        columns = ['id', 'status', 'date', 'home', 'away', 'home_score', 'away_score', 'home_point', 'away_point']
        for game in self.schedule.games:
            if (game.status in ['Final', 'In Progress']) and (game.home in div_list):
                current_game = [game.id, game.status, game.date, game.home, game.away, 
                                    game.home_score, game.away_score, game.home_point, game.away_point]
                games_list.append (current_game)
        # print (len(games_list))
        games_list_df = pd.DataFrame(games_list, columns= columns)
        # print (games_list_df)
        return games_list_df

    def get_teams (self):
        teams_list = []
        for team in self.league.teams:
            if team.division == self.division:
                teams_list.append(team.name)
        teams_list_df = pd.DataFrame(teams_list, columns=['Teams'])
        # print (teams_list_df)
        return teams_list

    def make_cube (self):
        #  the left is HOME and the TOP is AWAY
        for index, row in self.games_list_df.iterrows(): 
            # print (row)
            lt = row['home']; tt = row['away']
            if row['home_score'] > row['away_score']:
                winner = 'home'
                # print (f"Game # {index} - The home (left) {lt} ({row['home_score']}) beat the away (top) {tt} ({row['away_score']})")
            else:
                winner = 'away'
                # print (f"Game # {index} - The home (left) {lt} ({row['home_score']}) lost to the away (top) {tt} ({row['away_score']})")
            
        # # READ THE CELL & WRITE TO THE CELL for TOP
            cell = self.cube.loc[lt, tt]  # FIND THE CELL
            if pd.isna(cell):  #  if cell is empty
                if winner == "home":
                    self.cube.at[lt, tt] = {'lt': 1, 'tt': 0}
                else:
                    self.cube.at[lt, tt] = {'lt': 0, 'tt': 1}
            else:  #  if cell is NOT empty
                left_record = cell['lt']; top_record = cell['tt']
                if winner == "home":
                    left_record += 1
                else:
                    top_record += 1
                self.cube.at[lt, tt] = {'lt': left_record, 'tt': top_record}

        # READ THE CELL & WRITE TO THE CELL for LEFT
            cell = self.cube.loc[tt, lt]  # FIND THE CELL
            if pd.isna(cell):  #  if cell is empty
                if winner == "home":
                    self.cube.at[tt, lt] = {'lt': 0, 'tt': 1}
                else:
                    self.cube.at[tt, lt] = {'lt': 1, 'tt': 0}
            else:
                top_record = cell['lt']; left_record = cell['tt']
                if winner == "home":
                    left_record += 1
                else:
                    top_record += 1
                self.cube.at[tt, lt] = {'lt': top_record, 'tt': left_record}
        return self.cube

if __name__ == '__main__':
    league = load_teams ()
    schedule = load_api_games ()
    North_Cube = Cube ('Scotia North', league, schedule)

    print(North_Cube)
    cube_df = North_Cube.make_cube()
    # html = cube_df.to_html()

    make_web ('nhl/templates/cube', cube_df)