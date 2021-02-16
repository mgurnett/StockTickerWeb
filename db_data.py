#from my_data import get_data, times_to_use
import sqlite3
from sqlite3 import Error
import datetime
# import pandas as pd

from configparser import ConfigParser
#Read config.ini file
config_object = ConfigParser()
config_object.read("ST_config.ini")

db_info = config_object["DATABASE"]
db_file_name = db_info ["db_file_name"]
DEBUG = db_info ["DEBUG"]
player_info = config_object["PLAYERS"]
initial_balance = player_info ["initial"]

# it is sqliteConnection that will be passed around because cursor can be gotten from it.
#cursor = sqliteConnection.cursor()

def open_db(db_file, debug=False):
    try:
        sqliteConnection = sqlite3.connect(db_file)
        if debug:
            print ('connected to ', db_file)
    except Error as e:
        print("e",e)
        return
    return sqliteConnection

def close_db(sqliteConnection):
    cursor = sqliteConnection.cursor()
    cursor.close()
    sqliteConnection.close()
    return

def player_list ():
    list_of_players = []
    sqliteConnection = open_db (db_file_name, debug=False)
    
    c = sqliteConnection.cursor()
    sqlite_select_query = """SELECT first FROM Players ORDER BY id;"""
    c.execute(sqlite_select_query)
    lop= c.fetchall()
    for l in lop:
        list_of_players.append (l[0])
    close_db(sqliteConnection)
    return list_of_players

def make_new_player (first_name):
    sqliteConnection = open_db (db_file_name, debug=False)
#     print ("making a new player with the name", first_name)
    c = sqliteConnection.cursor()
#     if DEBUG: print (first_name)
    c.execute("INSERT INTO Players (First, Balance) VALUES (?, ?)",
              (first_name, initial_balance))
    sqliteConnection.commit()
    close_db(sqliteConnection)
    return

#==============  Open the database, get data and close the data base returning the data
def get_player_data(cursor, debug=False):
        
    sqlite_select_query = """SELECT * FROM players ORDER BY id;"""
    cursor.execute(sqlite_select_query)
#     records = cursor.fetchall()
    data_players = cursor.fetchall()
#     data_players = data.to_dict('records')   #<------- class 'list'
    if debug:
        print ('data_record is of type:', type (data_players))
        print ('data_record is:', data_players)
    
    return data_players

#==============  Open the database, get data and close the data base returning the data
def get_player_logs(cursor, player, debug):
    try:        
        if player == 0:
            sqlite_select_query = """SELECT * FROM Ledger    ORDER BY date;"""
        else:
            sqlite_select_query = """SELECT * FROM Ledger WHERE Player = 1 ORDER BY date DESC;"""
            
        cursor.execute(sqlite_select_query)
        player_logs = cursor.fetchall()
        if debug:
            print ('player_logs is of type:', type (player_logs))
            print ('player_logs is:', player_logs)
    
    except Error as e:
        print("e",e)

    return player_logs