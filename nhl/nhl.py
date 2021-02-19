import requests
# URL = 'https://statsapi.web.nhl.com/api/v1/teams/22'
# response = requests.get(URL)
# # print(response)
# #https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md#standings
# #https://www.kevinsidwar.com/iot/2017/7/1/the-undocumented-nhl-stats-api
# 
# r = requests.get(URL)
# 
# data = r.json() # as its a rest api you can directly access the json object 

# print(data)
# print (type(data))
# print (data.keys())
# print (type(data.keys()))
# teams = data.get('teams')
# print (type(teams))
# local = teams[0]
# print (local.keys())
# print (local.get('teamName'))

# teamname = data.get('teams')[0].get('teamName')
# print (teamname)

URL = 'https://statsapi.web.nhl.com/api/v1/standings?season=20192020'
response = requests.get(URL)
r = requests.get(URL)
data = r.json()
records = data.get('records')[0]['teamRecords']
print (records)