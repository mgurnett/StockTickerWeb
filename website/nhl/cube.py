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
        csv_df = pd.read_csv("nhl/templates/all_games.csv")
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
make_web ('nhl/templates/cube', North_Cube.cube)
# print (North_Cube.games_df)
#  the left is HOME and the TOP is AWAY
for index, row in North_Cube.games_df.iterrows(): 
    ht = row['home_team']; at = row['away_team']
    if row['home_point'] > row['away_point']:
        winner = 'home'
        print (f"Game # {index} - The home (left) {ht} ({row['home_point']}) beat the {at} ({row['away_point']})")
    else:
        winner = 'away'
        print (f"Game # {index} - The away (top) {at} ({row['away_point']}) beat the {ht} ({row['home_point']})")
    
    cell = North_Cube.cube.loc[ht, at]
    # if pd.isna(cell):  #  if cell is empty


'''
    
    ht = row['home_team']; at = row['away_team']
    for i in range(2):
        if i == 0:
            top_team = ht; left_team = at
        else:
            top_team = at; left_team = ht
        

            cell = North_Cube.cube.loc[top_team, left_team]
            if pd.isna(cell):
                North_Cube.cube.at[top_team, left_team] = {'at': 0, 'ht': 1}
            else:
                a_record = cell['at']
                h_record = cell['ht'] + 1
                North_Cube.cube.at[top_team, left_team] = {'at': a_record, 'ht': h_record}

            cell = North_Cube.cube.loc[top_team, left_team]
            if pd.isna(cell):
                North_Cube.cube.at[top_team, at] = {'at': 1, 'ht': 0}
            else:
                a_record = cell['at'] + 1
                h_record = cell['ht']
                North_Cube.cube.at[top_team, left_team] = {'at': a_record, 'ht': h_record}
    print (North_Cube.cube)
    if index == 10:
        break
    '''