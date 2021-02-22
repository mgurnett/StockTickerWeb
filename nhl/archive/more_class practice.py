class Teams:
    def __init__ (self):
        self.teams_all = []
        self.id = 0
        self.teamName = ""
        self.venue = ""
        self.city = ""
        
    def add_team (self, id):
        for i, t in enumerate (self.teams_all):
            if t.id == id:  #old team
                index = i
                print ('team already there')
            else:
                self.teams_all.append(id)  #new team
                index = i
                print ('team added')
        return
    
#     def __str__ (self):
#         return f"The {self.city} {self.teamName} ({self.id}) play in {self.venue}."

teams = Teams()
id = 22
teams.add_team (id)
print (teams.id)
print (teams.teams_all)
    
    
# id = 22
# team_list.append (Team (id))
# team_list[0].teamName = "Oilers"
# team_list[0].city = "Edmonton"
# team_list[0].venue = "Rogers Place"
# 

# 
# print (team_list[0].__format__)