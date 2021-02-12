from db_data import *
from ST_classes_NEW import *
import datetime
import sqlite3
from sqlite3 import Error
from yahoo_fin import stock_info as si

import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt

from configparser import ConfigParser

playerlist = Player.player_list()
# print (playerlist)
results = []; total_value = 0

for player in playerlist:
    local_worth = Player(player).calculate_networth()
    print(player, "is worth", Player.money_str(local_worth))
    results.append(local_worth)
    total_value =total_value + local_worth
    
average_value = total_value / len(results)
print ('Total value is {} and Average value is {}'.format(total_value, average_value))


fig = plt.figure(figsize = (10, 5)) 
plt.bar(playerlist,results, color ='maroon', width = 0.4)
plt.xlabel("Players") 
plt.ylabel("Networth") 
plt.title("Stock Ticker")

# specifying horizontal line type 
plt.axhline(y = int(Player.start_balance), color = 'r', linestyle = '-')
plt.axhline(y = int(average_value), color = 'g', linestyle = '-') 
plt.show()