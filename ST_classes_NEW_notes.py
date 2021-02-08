from db_data import *
import datetime
import sqlite3
from sqlite3 import Error
from yahoo_fin import stock_info as si

import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

from configparser import ConfigParser
# Read config.ini file
config_object = ConfigParser()
config_object.read("ST_config.ini")

player_info = config_object["PLAYERS"]
initial_balance = player_info["initial"]


class Player ():
    start_balance = initial_balance

    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.transaction_symbol = ""
        self.transaction_amount = 0
        # this starts whenever the class is called.
        self.id = self.setup_player()
        self.current_date = int(datetime.datetime.now().strftime('%s'))

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
        print ("from the class", self.name)
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

    def purchase_timestamp_str(self, date_time):
        dt = datetime.datetime.fromtimestamp(date_time)
        return dt.strftime("%a, %e %b %Y - %l:%M %p")

    def purchase_shares(self):
        ps_id = current_player.id
        ps_volume = self.transaction_amount
        ps_symbol = self.transaction_symbol
        ps_price = Player.current_price(ps_symbol)
        print(current_player.name_balance_str(), "(", ps_id, ") wants to purchase",  ps_volume, "of",
              Player.stock_full_name(ps_symbol), "with a purchase price of",
              Player.money_str(Player.current_price(ps_symbol)))

        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()

        c.execute("INSERT INTO Portfolio (stock, player, number, purchase_price) VALUES (?, ?, ?, ?)",
                  (ps_symbol, ps_id, ps_volume, ps_price))

        c.execute("INSERT INTO Ledger (Ticker, Price, Volume, Player, date, action ) VALUES (?, ?, ?, ?, ?, ?)",
                  (ps_symbol, ps_price, ps_volume,
                   ps_id,  datetime.datetime.now().strftime('%s'), "buy"))

        self.balance = self.balance - (ps_price * ps_volume)
        c.execute("UPDATE Players SET Balance = ? WHERE id = ?",
                  (self.balance, ps_id))

        sqliteConnection.commit()
        close_db(sqliteConnection)
        return

    def sell_shares(self):
        ss_id = current_player.id
        ss_volume = self.transaction_amount
        ss_symbol = self.transaction_symbol
        ss_price = Player.current_price(ss_symbol)
        print(current_player.name_balance_str(), "(", ss_id, ") wants to sell",  ss_volume, "of",
              Player.stock_full_name(ss_symbol), "with a current price of",
              Player.money_str(ss_price),
              "They have", current_player.balance_str(),
              ". The total sell price is", Player.money_str(
            ss_volume * ss_price),
            "leaving a new balance of", Player.money_str(
            current_player.balance + (ss_volume * ss_price))
        )

        sqliteConnection = open_db(db_file_name, debug=False)
        c = sqliteConnection.cursor()

        c.execute(
            "SELECT number FROM Portfolio WHERE stock = ? AND player = ?", (ss_symbol, ss_id))
        port_num = c.fetchone()

        ss_stock_owned = port_num[0]
        ss_stock_left = ss_stock_owned - ss_volume

        if ss_stock_left > 0:
            c.execute("UPDATE Portfolio SET number = ? WHERE stock = ? AND player = ?",
                      (ss_stock_left, ss_symbol, ss_id))
        else:
            c.execute(
                "DELETE FROM Portfolio WHERE stock = ? AND player = ?", (ss_symbol, ss_id))

        c.execute("INSERT INTO Ledger (Ticker, Price, Volume, Player, date, action ) VALUES (?, ?, ?, ?, ?, ?)",
                  (ss_symbol, ss_price, ss_volume, ss_id, datetime.datetime.now().strftime('%s'), "sell"))

        current_player.balance = current_player.balance + \
            (ss_volume * ss_price)

        c.execute("UPDATE Players SET Balance = ? WHERE id = ?",
                  (current_player.balance, ss_id))

        sqliteConnection.commit()
        close_db(sqliteConnection)
        return


# current_player = Player ("Computer dumb")
# #
# # print (current_player.purchase_timestamp_str(current_player.current_date))
# #
# # print (current_player.name_balance_str(), " & ",
# #        current_player.balance_str(), " @ ",
# #        current_player.purchase_timestamp_str(current_player.current_date))
#
# portfolio = current_player.load_portfolio()
# # print (portfolio[1][1])
# ledger = current_player.load_ledger()
# # print (current_player.purchase_timestamp_str(ledger[1][5]))
# worth = current_player.calculate_networth()
#
# price = Player.current_price ("aapl")
#
#
#
playerlist = Player.player_list()
# print (playerlist)
results = []; total_value = 0

for player in playerlist:
    local_worth = Player(player).calculate_networth()
    print(player, "is worth", Player.money_str(local_worth))
    results.append(local_worth)
    total_value =total_value + local_worth
    
average_value = total_value / len(results)
print (total_value, average_value)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(playerlist,results)

# specifying horizontal line type 
plt.axhline(y = int(Player.start_balance), color = 'r', linestyle = '-')
plt.axhline(y = int(average_value), color = 'g', linestyle = '-') 
plt.show()
# current_player = Player("rabbit")
# # print (current_player.name_balance_str(), " & ",
# #        current_player.balance_str(), " @ ",
# #        current_player.purchase_timestamp_str(current_player.current_date))
# current_player.transaction_amount = 2
# current_player.transaction_symbol = "aapl"
# print("full name", Player.stock_full_name(current_player.transaction_symbol))
# current_player.purchase_shares()

# current_player = Player("rabbit")
# # print (current_player.name_balance_str(), " & ",
# #        current_player.balance_str(), " @ ",
# #        current_player.purchase_timestamp_str(current_player.current_date))
# current_player.transaction_amount = 2
# current_player.transaction_symbol = "aapl"
# print("full name", Player.stock_full_name(current_player.transaction_symbol))
# current_player.sell_shares()

current_stock = Stock('f')
print (current_stock.full_name())