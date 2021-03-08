from db_data import *
from ST_classes_MAIN import *
import numpy as np

current_stock = Stock("aapl")
current_player = Player ("history Apple")

current_player.transaction_symbol = current_stock.symbol
stock_data = current_stock.price_history(4000)

def how_much_to_buy (c_player, price):
    balance = c_player.balance
    to_buy = int(balance/price)
    return to_buy

def how_much_to_sell (c_player):
    to_sell = 0
    log = current_player.load_portfolio()
    for l in log:
        if l[1] == current_player.transaction_symbol:
            to_sell = l[3]
    return to_sell

for d, row in stock_data.iterrows():
#     print (row)
    if np.isnan(row['Buy_Signal_Price']):
        pass
    else:
        purchase_price = row['Buy_Signal_Price']
        purchase_date = str(d)
        amount = how_much_to_buy (current_player, purchase_price)
        current_player.transaction_amount = amount
        current_player.purchase_shares (historical_price = purchase_price, historical_date = purchase_date)
        print ('{} bought {} ({}) at {} on {}'.format(current_player.name,
                                                      current_stock.full_name(),
                                                      current_stock.symbol,
                                                      purchase_price,
                                                      purchase_date))

    if np.isnan(row['Sell_Signal_Price']):
        pass
    else:
        sell_price = row['Sell_Signal_Price']
        sell_date = str(d)
        amount = how_much_to_sell (current_player)
        current_player.transaction_amount = amount
        if amount >0:
            current_player.sell_shares (historical_price = sell_price, historical_date = sell_date)
        print ('{} sold {} ({}) at {} on {}'.format(current_player.name,
                                                      current_stock.full_name(),
                                                      current_stock.symbol,
                                                      sell_price,
                                                      sell_date))


        

        

# current_player = Player('Garbage')
# current_stock = Stock('aapl')
# current_player.transaction_symbol = current_stock.symbol
# current_player.transaction_amount = 1
# purchase_date = str('2018-02-12 09:07:56')
# 
# print ('{} bought {} ({}) at {} on {}'.format(current_player.name,
#                                               current_stock.full_name(),
#                                               current_stock.symbol,
#                                               current_stock.current_price(),
#                                               purchase_date))
# 
# current_player.purchase_shares (historical_price = 123.45, historical_date = str('2018-02-12 09:07:56'))



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

# current_stock = Stock('f')
# print (current_stock.full_name())