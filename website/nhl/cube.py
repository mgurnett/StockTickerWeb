import pandas as pd
from makeweb import make_web

class Cube:
    def __init__ (self, division):
        self.division = division
        self.games_df = self.get_games()
        self.teams_list = self.get_teams()
        self.cube = pd.DataFrame ({'h':0, 'a':0},columns=self.teams_list, index=self.teams_list)

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
        print (f'The {ht} beat the {at} at home')
        North_Cube.cube.at['ht', 'at'] = {'h':1, 'a':0}
    else:
        winner = 'away'
        print (f'The {ht} lost to the {at} at home')
        North_Cube.cube.at['ht', 'at'] = {'h':0, 'a':1}

