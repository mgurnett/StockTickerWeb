from db_data import *
# from scrapping import *
import datetime
from datetime import timedelta
import sqlite3
from sqlite3 import Error
from yahoo_fin import stock_info as si
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

from configparser import ConfigParser
# Read config.ini file
config_object = ConfigParser()
config_object.read("ST_config.ini")

player_info = config_object["PLAYERS"]
initial_balance = player_info["initial"]

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
DISPLAY_FORMAT = "%a, %e %b %Y -%l:%M %p"

class Player ():
    start_balance = initial_balance

    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transaction_symbol = ""
        self.transaction_amount = 0
        self.current_date_e = int(datetime.datetime.now().timestamp())
        # this starts whenever the class is called.
        self.id = self.setup_player()

    @staticmethod
    def player_list():
        list_of_players = []
        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()
        sqlite_select_query = """SELECT first FROM Players ORDER BY id;"""
        c.execute(sqlite_select_query)
        lop = c.fetchall()
        for l in lop:
            list_of_players.append(l[0])
        close_db(sqliteConnection)
        return list_of_players

    @staticmethod
    def money_str(value):
        return "${:,.2f}".format(value)

    @staticmethod
    def stock_full_name(symbol):
        URL = "https://www.google.com/search?q="+symbol+"&tbm=fin"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        page = requests.get(URL, headers=headers)
#         print (symbol, page)
        soup = bs(page.content, "html.parser")
        try:
            name = soup.find('span', attrs={'class': "mfMhoc"}).text
        except:
            name = ""
        return name

    @staticmethod
    def current_price(symbol):  # this should be static too
        try:
            current_stock_price = si.get_live_price(symbol)
        except:
            current_stock_price = 0
        return current_stock_price

    def __repr__(self):  # use for troubleshooting
        return "${:,.2f}".format(self.balance)

    def balance_str(self):
        return "${:,.2f}".format(self.balance)

    def name_balance_str(self):
        return "{} ({})".format(self.name, self.balance_str())

    # This looks for a player in the database and gets it's ID.
    def setup_player(self):
        # if there isn't that player, then it creates it and gets the new ID.
#         print ("from the class", self.name)
        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()
        c.execute("SELECT id, balance FROM Players WHERE First = ?",
                  (self.name, ))  # some reason the , has to be there
        try:  # see if there is a player
            player_info = c.fetchone()
            playerID = player_info[0]
            self.balance = player_info[1]
        except:  # if not, then make one
            sqliteConnection = open_db(db_file_name, debug=False)
            c = sqliteConnection.cursor()
            c.execute("INSERT INTO Players (First, Balance) VALUES (?, ?)",
                      (self.name, Player.start_balance))
            c.execute("SELECT id FROM Players WHERE First = ?",
                      (self.name, ))
            player_id = c.fetchone()
            playerID = player_id[0]
            sqliteConnection.commit()
            close_db(sqliteConnection)
        return playerID

    def load_portfolio(self):
        sqliteConnection = open_db(db_file_name, debug=False)  # open DB
        c = sqliteConnection.cursor()
        # the comma needs to be there.
        c.execute(
            "SELECT * FROM Portfolio WHERE player = ? ORDER BY stock", (self.id, ))
        portfolio_list = c.fetchall()
        close_db(sqliteConnection)  # close DB
        # print (portfolio[1][1]) gets you the symbol of second stock
        return portfolio_list

    def load_ledger(self):
        sqliteConnection = open_db(db_file_name, debug=False)  # open DB
        c = sqliteConnection.cursor()
        # the comma needs to be there.
        c.execute(
            "SELECT * FROM Ledger WHERE player = ? ORDER BY date DESC", (self.id, ))
        ledger_list = c.fetchall()
        close_db(sqliteConnection)  # close DB
        return ledger_list

    def calculate_networth(self):
        port_list = self.load_portfolio()
        nw = self.balance
        for p in port_list:
            nw = nw + p[3] * Player.current_price(p[1])
        return nw

    def timestamp_str_from_e (self, date_time):
        dt = datetime.datetime.fromtimestamp(date_time)
        return str(dt)

    def timestamp_str_to_e (self, date_time):
        epoch = datetime.datetime(1970, 1, 1)
        tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        if tz_string == 'MST':
            tz_comp = 25200
        else:
            tz_comp = 28800
        epoch_time = (datetime.datetime.strptime(date_time, TIMESTAMP_FORMAT) - epoch).total_seconds() + tz_comp
        return int(epoch_time)
    
    def purchase_shares(self, **kwargs):
        ps_id = self.id
        ps_volume = self.transaction_amount
        ps_symbol = self.transaction_symbol
        
        ps_price = kwargs.get("historical_price", Player.current_price(ps_symbol))
        # either the price sent in via historical_price = 25 or default to current price
        cur_datetime = datetime.datetime.now().replace(microsecond=0) # now time without the microseconds
        p_date  = kwargs.get("historical_date", str(cur_datetime))
        # either the date sent in via historical_date = str('2018-02-12 09:07:56') or default to datetime.now
        ps_date = self.timestamp_str_to_e (p_date)

#         print(self.name_balance_str(), "(", ps_id, ") wants to purchase",  ps_volume, "of",
#               Player.stock_full_name(ps_symbol), "with a purchase price of",
#               Player.money_str(ps_price))
        
        print ("cur_datetime is {}".format(cur_datetime))
        print ("p_date is {}".format(p_date))
        print ("ps_date is {}".format(ps_date))
        print ("ps_date is {}".format(self.timestamp_str_from_e(ps_date)))

        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()

        c.execute("INSERT INTO Portfolio (stock, player, number, purchase_price) VALUES (?, ?, ?, ?)",
                  (ps_symbol, ps_id, ps_volume, ps_price))

        c.execute("INSERT INTO Ledger (Ticker, Price, Volume, Player, date, action ) VALUES (?, ?, ?, ?, ?, ?)",
                  (ps_symbol, ps_price, ps_volume, ps_id,  ps_date, "buy"))

#         print ('balance is {} minus {} * {}'.format(type(self.balance), type(ps_price), type(ps_volume)))
        self.balance = self.balance - (ps_price * ps_volume)
        c.execute("UPDATE Players SET Balance = ? WHERE id = ?",
                  (self.balance, ps_id))

        sqliteConnection.commit()
#         close_db(sqliteConnection)
#===========   need to make a consolidation pass or change how stock is added to the portfolio, by adding if it exists
        return

    def sell_shares(self, **kwargs):
        ss_id = self.id
        ss_volume = self.transaction_amount
        ss_symbol = self.transaction_symbol
        ss_price = kwargs.get("historical_price", Player.current_price(ss_symbol))
        # either the price sent in via historical_price = 25 or default to current price
#         cur_datetime = datetime.datetime.now().replace(microsecond=0) # now time without the microseconds
        cur_datetime = self.timestamp_str_from_e(self.current_date_e)
        s_date  = kwargs.get("historical_date", str(cur_datetime))
        # either the date sent in via historical_date = str('2018-02-12 09:07:56') or default to datetime.now
        ss_date = self.timestamp_str_to_e (s_date)
        
        print ('{} ({}) wants to sell {} of {} with a price of {}.  They have {}.'.
               format(self.name_balance_str(), ss_id, ss_volume,
                      Player.stock_full_name(ss_symbol), Player.money_str(ss_price), self.balance_str()))
        print ('The total sell price is {} leaving a new balance of {}'.
               format(Player.money_str( ss_volume * ss_price), Player.money_str( self.balance + (ss_volume * ss_price))))
        
        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()

        c.execute(
            "SELECT number FROM Portfolio WHERE stock = ? AND player = ?", (ss_symbol, ss_id))
        port_num = c.fetchone()

        ss_stock_owned = port_num[0]
        print ('ss_stock_owned is {}'.format( ss_stock_owned ))
        ss_stock_left = ss_stock_owned - ss_volume
        print ('ss_stock_left is {}'.format( ss_stock_left ))

        if ss_stock_left > 0:
            c.execute("UPDATE Portfolio SET number = ? WHERE stock = ? AND player = ?",
                      (ss_stock_left, ss_symbol, ss_id))
        else:
            c.execute(
                "DELETE FROM Portfolio WHERE stock = ? AND player = ?", (ss_symbol, ss_id))

        c.execute("INSERT INTO Ledger (Ticker, Price, Volume, Player, date, action ) VALUES (?, ?, ?, ?, ?, ?)",
                  (ss_symbol, ss_price, ss_volume, ss_id, ss_date, "sell"))

        self.balance = self.balance + (ss_volume * ss_price)

        c.execute("UPDATE Players SET Balance = ? WHERE id = ?",
                  (self.balance, ss_id))

        sqliteConnection.commit()
#         close_db(sqliteConnection)
        return
    
#======================================================   
class Stock ():
    def __init__(self, symbol):
        self.symbol = symbol
#         print ("From Stock CLASS: ", symbol)

    @staticmethod
    def smoney_str(value):
        return "${:,.2f}".format(value)
        
    def current_price(self):
        try:
            current_stock_price = si.get_live_price(self.symbol)
        except:
            current_stock_price = ""
        return current_stock_price
        
    def price_history(self, days):
        try:
            stock_data = si.get_data(self.symbol)
            start_date = datetime.datetime.today() - timedelta(days=days)
            current_stock_data = stock_data.tail(days)
            current_stock_data['SMA30'] = stock_data ['adjclose'].rolling (window = 30).mean()   
            current_stock_data['SMA100'] = stock_data ['adjclose'].rolling (window = 100).mean()
#             print (current_stock_data)
            sigPriceBuy = []
            sigPriceSell = []
            flag = -1

            for i in range(len(current_stock_data)):
                if current_stock_data['SMA30'][i] > current_stock_data['SMA100'][i]:
                    if flag != 1:
                        sigPriceBuy.append(current_stock_data['adjclose'][i])
                        sigPriceSell.append(np.nan)
                        flag = 1
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                elif current_stock_data['SMA30'][i] < current_stock_data['SMA100'][i]:
                    if flag != 0:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(current_stock_data['adjclose'][i])
                        flag = 0
                    else:
                        sigPriceBuy.append(np.nan)
                        sigPriceSell.append(np.nan)
                else:
                    sigPriceBuy.append(np.nan)
                    sigPriceSell.append(np.nan)
            current_stock_data.loc[:,'Buy_Signal_Price'] = sigPriceBuy
            current_stock_data.loc[:,'Sell_Signal_Price'] = sigPriceSell

        except Exception as e:
            print(e)
            current_stock_data = "no go"
        return current_stock_data
    
    def full_name(self):
        symbol = self.symbol
        URL = "https://ca.finance.yahoo.com/quote/{}?p=".format(symbol)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        page = requests.get(URL, headers=headers)
        soup = bs(page.content, "html.parser")
        try:
            name=soup.find ('h1', attrs = {'class':"D(ib) Fz(18px)"}).text
            large_name = name[:name.index(" (")]
        except:
            large_name = ""
        return large_name