import pandas as pd
from makeweb import make_web

class Cube:
    def __init__ (self, division, all_the_games_df):
        self.division = division
        self.all_the_games_df = all_the_games_df
        self.games_df = self.get_games()
        self.teams_list = self.get_teams()
        self.cube = pd.DataFrame ({'tt': 0, 'lt': 0},columns=self.teams_list, index=self.teams_list)

    def get_games (self):
        # csv_df = pd.read_csv("nhl/templates/all_games.csv")
        csv_df = self.all_the_games_df
        temp_df = csv_df[csv_df['Division'] == self.division]
        return temp_df

    def get_teams (self):
        temp_df = self.games_df.drop_duplicates(subset=['home_team'])
        temp_list = temp_df[["home_team"]].values.tolist()
        teams_list = []
        for t in temp_list:
            teams_list.append(t[0])
        return teams_list

    def make_cube (self):
        #  the left is HOME and the TOP is AWAY
        for index, row in self.games_df.iterrows(): 
            lt = row['home_team']; tt = row['away_team']
            if row['home_point'] > row['away_point']:
                winner = 'home'
                # print (f"Game # {index} - The home (left) {lt} ({row['home_point']}) beat the home (top) {tt} ({row['away_point']})")
            else:
                winner = 'away'
                # print (f"Game # {index} - The home (left) {lt} ({row['home_point']}) lost to the away (top) {tt} ({row['away_point']})")
            
        # READ THE CELL & WRITE TO THE CELL for TOP
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

# if __name__ == '__main__':
#     North_Cube = Cube ('Scotia North')
#     cube_df = North_Cube.make_cube()
#     make_web ('nhl/templates/cube', cube_df)