from ST_classes_MAIN import *

current_player = Player ("Garbage")
current_stock = Stock('f')

current_player.transaction_amount = 1
current_player.transaction_symbol = current_stock.symbol

#======== Buy stock now at the current price
# print ('At {}, {} wants to buy {} of {} ({}) @ {} a share for a total of {}'
#        .format(current_player.timestamp_str_from_e (current_player.current_date),
#                current_player.name_balance_str(),
#                current_player.transaction_amount,
#                current_stock.full_name(),
#                current_stock.symbol,
#                Player.money_str(current_stock.current_price()),
#                Player.money_str(current_stock.current_price() * current_player.transaction_amount)
#                ))
# 
# current_player.purchase_shares()

#======== Buy stock in the past with a madeup price
# purchase_date = str('2018-02-12 09:07:56')
# print ('At {}, {} wants to buy {} of {} ({}) @ {} a share for a total of {}'
#        .format(purchase_date,
#                current_player.name_balance_str(),
#                current_player.transaction_amount,
#                current_stock.full_name(),
#                current_stock.symbol,
#                Player.money_str(current_stock.current_price()),
#                Player.money_str(current_stock.current_price() * current_player.transaction_amount)
#                ))
# current_player.purchase_shares (historical_price = 123.45, historical_date = purchase_date)

# purchase_date = str('2018-02-12 09:07:56')

#======== sell stock now at the current price
# purchase_date = current_player.timestamp_str_from_e (current_player.current_date)
# print ('At {}, {} wants to sell {} of {} ({}) @ {} a share for a total of {}'
#        .format(purchase_date,
#                current_player.name_balance_str(),
#                current_player.transaction_amount,
#                current_stock.full_name(),
#                current_stock.symbol,
#                Player.money_str(current_stock.current_price()),
#                Player.money_str(current_stock.current_price() * current_player.transaction_amount)
#                ))
# current_player.sell_shares ()

#======== sell stock now at the current price
# purchase_date = str('2018-02-12 09:07:56')
# print ('At {}, {} wants to sell {} of {} ({}) @ {} a share for a total of {}'
#        .format(purchase_date,
#                current_player.name_balance_str(),
#                current_player.transaction_amount,
#                current_stock.full_name(),
#                current_stock.symbol,
#                Player.money_str(current_stock.current_price()),
#                Player.money_str(current_stock.current_price() * current_player.transaction_amount)
#                ))
# current_player.sell_shares (historical_price = 1230.45, historical_date = purchase_date)

COMMON = [("aapl", "Apple Inc"),
          ("ac", "Air Canada"),
          ("amzn", "Amazon.com, Inc."),
          ("ba", "Boeing Co"),
          ("ccl", "Carnival Corp"),
          ("coke", "Coca-Cola Consolidated Inc"),
          ("f", "Ford"),
          ("fb", "Facebook, Inc. Common Stock"),
          ("goog", "Alphabet Inc Class C"),
          ("gme", "Gamestop"),
          ("mar", "Marriott International"),
          ("msft", "Microsoft"),
          ("nflx", "Netflix Inc"),
          ("su", "Suncor Energy Inc."),
          ("tsla", "Tesla Inc"),
          ("zm", "Zoom Video Com")]

for c in COMMON:
    current_stock = Stock(c[0])
    name  = current_stock.full_name()
    print (name)