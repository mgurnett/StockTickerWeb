from db_data import *
from ST_classes_NEW import *

current_stock = Stock("aapl")
current_player = Player ("computer smart")

current_player.transaction_amount = 2
current_player.transaction_symbol = "aapl"
# current_player.purchase_shares(historical_price=123.45)
stock_data = current_stock.price_history(30)
print (type(stock_data))
print (stock_data)
for d, row in stock_data.iterrows():
    print (d, row['adjclose'], row['Buy_Signal_Price'], row['Sell_Signal_Price'])

current_player.purchase_shares(historical_price=123.45, historical_date='2021-02-11 00:00:00')