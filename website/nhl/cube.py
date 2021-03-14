import pandas as pd
from makeweb import make_web

class Cube:
    def __init__ (self, division):
        self.division = division
        self.games_df = self.get_games()
        self.teams_list = self.get_teams()
        self.cube = pd.DataFrame ({'at': 0, 'ht': 0},columns=self.teams_list, index=self.teams_list)
        # self.cube = pd.DataFrame (0,columns=self.teams_list, index=self.teams_list)

    def get_games (self):
        csv_df = pd.read_csv("all_games.csv")
        temp_df = csv_df[csv_df['Division'] == self.division]
        return temp_df

    def get_teams (self):
        temp_df = self.games_df.drop_duplicates(subset=['home_team'])
        temp_list = temp_df[["home_team"]].values.tolist()
        teams_list = []
        for t in temp_list:
            teams_list.append(t[0])
        return teams_list

North_Cube = Cube ('Scotia North')
# print (North_Cube.cube)  <-- this is a DataFrame
make_web ('cube', North_Cube.cube)
# print (North_Cube.games_df)
for index, row in North_Cube.games_df.iterrows(): 
    # print (row['home_team'], row['home_point'], row['away_team'], row['away_point'])
    ht = row['home_team']; at = row['away_team']
    if row['home_point'] > row['away_point']:
        winner = 'home'
        print (f'Game # {index} - The {ht} beat the {at} at home and the winner was {winner}')
        cell = North_Cube.cube.loc[ht, at]
        if pd.isna(cell):
            North_Cube.cube.at[ht, at] = {'at': 0, 'ht': 1}
        else:
            a_record = cell['at']
            h_record = cell['ht'] + 1
            North_Cube.cube.at[ht, at] = {'at': a_record, 'ht': h_record}
    else:
        winner = 'away'
        print (f'Game # {index} - The {ht} beat the {at} at home and the winner was {winner}')
        cell = North_Cube.cube.loc[ht, at]
        if pd.isna(cell):
            North_Cube.cube.at[ht, at] = {'at': 1, 'ht': 0}
        else:
            a_record = cell['at'] + 1
            h_record = cell['ht']
            North_Cube.cube.at[ht, at] = {'at': a_record, 'ht': h_record}
    print (North_Cube.cube)
    if index == 10:
        break