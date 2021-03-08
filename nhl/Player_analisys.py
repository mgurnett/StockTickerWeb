import pandas as pd
# import json

from pretty_html_table import build_table

# Set up the API call variables
year = '2020'
season_type = '02' 
max_game_ID = 300
base_URL = "https://statsapi.web.nhl.com/api/v1/"

def make_web (name, df):
    html_table = build_table(df, 'blue_dark')
    file_name = ('games_folder/' + name + ".html")
    text_file = open(file_name, "w")
    text_file.write(html_table)
    text_file.close()

all_players_df = pd.read_pickle('players_df.pkl')
# make_web ('players', all_players_df)

scorers = all_players_df.sort_values(by=['goals', 'assists'], ascending=False).head(10)
make_web ('scorers', scorers)

defence = all_players_df.groupby(["primaryPosition_name"]).get_group(("Defenseman"))
d_points = defence.sort_values(by=['points', 'goals'], ascending=False).head(10)
d_points_sub = d_points[['firstName', 'lastName', 'currentTeam', 'points', 'goals', 'assists']]
make_web ('d_points_sub', d_points_sub)

points = all_players_df.sort_values(by=['points', 'goals'], ascending=False).head(10)
make_web ('points', points)

plusMinus = all_players_df.sort_values(by=['plusMinus'], ascending=False).head(10)
make_web ('plusMinus', plusMinus)
# print (all_players_df.dtypes)
# print (all_players_df.describe())
sub_df = all_players_df[['firstName', 'lastName', 'currentTeam', 'points', 'goals', 'assists']]
# make_web ('players_sub', sub_df)