from db_data import *
from scrapping import *
# from tkinter import ttk 
# import tkinter as tk 
# import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si
# import yahoo_fin.stock_info as si_info
import numpy as np
from configparser import ConfigParser
#Read config.ini file
config_object = ConfigParser()
config_object.read("ST_config.ini")

player_info = config_object["PLAYERS"]
initial_balance = player_info ["initial"]
DEBUG = db_info ["DEBUG"]
colour = config_object["COLOURS"]
_frame_color = colour["frame_color"]
_message_color = colour["message_color"]
_canvas_color = colour["canvas_color"]
_root_color = colour["root_color"]

class Player:
    def __init__(self, name):
        self.name = name
        self.amount = 0
#         print ("The name of the player to be used is:", self.name)

    def create_player_in_db(self):
        list_of_players = player_list ()
      
        #check to see if the player's name is already in the list
        if self.name in list_of_players:
            #if yes return - name already used
            print('The name', self.name, 'is already used')
        else:
            #if no return - name added to player list
            #create a new player in SQlite
            make_new_player (self.name)

    def check_balance(self):
        #open DB
        sqliteConnection = open_db (db_file_name, debug=False)
        c = sqliteConnection.cursor()
        name = self.name
#         if DEBUG: print (name)
        c.execute("SELECT Balance FROM Players WHERE First = ?", (name,))
        balance = c.fetchone()
        #close DB
        close_db(sqliteConnection)
        return balance[0]

    def portfolio_worth(self):
        port_worth = 0
        portfolio_log = self.portfolio()
        for p in portfolio_log:
            stock_symb = p[1]
            stock = Stock (stock_symb)
            price = stock.current_price()
            port_worth = port_worth + (price * p[3])

        return port_worth
   
    def buy_shares(self, local_stock):
        name = self.name
        balance = self.check_balance()
        temp_price = local_stock.current_price()
        price = temp_price.item()
        amount = int(self.amount)

        if (price*amount) > balance:
            print ("Sorry, too much")
        else:
            buy_shares (local_stock, self)

    def sell_shares(self, local_stock, amount_left, to_sell):
        name = self.name
#         balance = self.check_balance()
#         temp_price = local_stock.current_price()
#         price = temp_price.item()

        sell_shares (self, local_stock, amount_left, to_sell)

    def track_shares(self):
        sqliteConnection = open_db (db_file_name, debug=False)        #open DB
        c = sqliteConnection.cursor()
        c.execute("SELECT id FROM Players WHERE First = ?", (self.name,))
        player_ids = c.fetchone(); player_id = player_ids[0]
        c.execute("SELECT * FROM Ledger WHERE player = ? ORDER BY date DESC", ( player_id, ))# the comma needs to be there.
        log_list = c.fetchall()
        close_db(sqliteConnection)        #close DB
        return log_list

    def portfolio(self):
        sqliteConnection = open_db (db_file_name, debug=False)        #open DB
        c = sqliteConnection.cursor()
        c.execute("SELECT id FROM Players WHERE First = ?", (self.name,))
        player_ids = c.fetchone(); player_id = player_ids[0]
        c.execute("SELECT * FROM Portfolio WHERE player = ? ORDER BY stock", ( player_id, ))# the comma needs to be there.
        portfolio_list = c.fetchall()
        close_db(sqliteConnection)  #close DB
        return portfolio_list
        
#===============================================
class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        
    def current_price(self):
        try:
            current_stock_price = si.get_live_price(self.symbol)
        except:
            current_stock_price = ""
        return current_stock_price
        
    def price_history(self):
        try:
            current_stock_data = si.get_data(self.symbol , start_date = '01/01/2010')
        except:
            current_stock_data = ""
        return current_stock_data
    
    def full_name (self):
        name  = get_stock_full_name(self.symbol)
        return name

# x= Stock ("goog")
# print (x)
# print (x.symbol)
# print (x.current_price())
# print (x.price_history())
# print (x.full_name())
# y = Player ("Michael")
# print (y.name)
# local_stock = Stock("goog")
# local_player = Player ("Michael")
# print (local_player.check_balance())
# 
# print (local_player.portfolio_worth())