from flask import Flask, render_template, request, make_response

import datetime
from db_data import *
from ST_classes_NEW import *

from io import BytesIO
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
plt.style.use('dark_background')

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

default_player = Player("Michael"); current_player = ""
default_stock = Stock("aapl"); current_stock = ""

app = Flask(__name__)

def main_loop():

    @app.route('/')
    def main():
        global current_player, current_stock
        
        player_id = request.args.get("name", None) #Michael is the default   127.0.0.1:5000/?name=michael
        if player_id == None:
#             print ("player - None", player_id)
#             print ("current_player", current_player)
            if current_player == "":
#                 print ('current_player = None')
                current_player = default_player
        else:
#             print ("player - NOT None", player_id)
            current_player = Player(player_id)
        
        stock_symb = request.args.get("stock", None) #aapl is the default   127.0.0.1:5000/?stock=aapl
        if stock_symb == None:
#             print ("stock - None", stock_symb, )
            if current_stock == "":
                stock_symb = "goog"
                current_stock = Stock(stock_symb)
#                 print ("stock - None2", current_stock.full_name())
        else:
#             print ("stock - NOT None", stock_symb)
            current_stock = Stock(stock_symb)
#             print ("stock - NOT None2", current_stock.full_name())
            
#         print ("player_id", player_id, "stock_symb", stock_symb)
#         print ("current_player", current_player.name, "current_stock", current_stock.symbol)
        
        title = "This is web based STOCK TICKER"
        return render_template ('index.html', title = title, common = COMMON,
                                player = current_player, Player = Player,
                                stock = current_stock, Stock = Stock)

    @app.route('/about')
    def about():
        global current_player
        return render_template ('about.html')

    @app.route('/newplayer')
    def newplayer():
        return render_template ('newplayer.html', player = current_player, Player=Player, common = COMMON, stock = current_stock,
                                Stock = Stock)

    @app.route('/form', methods=["POST"])
    def form():
        global current_player
        name = request.form.get ("name")
        current_player = Player (name)
        return render_template ('form.html', player = current_player, Player=Player, common = COMMON, stock = current_stock,
                                Stock = Stock)

    @app.route('/search_stock', methods=["POST"])
    def search_stock():
        global current_stock
#         query = request.args['search']
        stock = request.form.get ("stock")
        print (stock)
        current_stock = Stock(stock)
        return render_template ('search_stock.html', player = current_player, Player=Player, common = COMMON, stock = current_stock,
                                Stock = Stock)

    @app.route('/networth')
    def networth():
        global current_player
        return render_template ('networth.html', player = current_player, Player=Player, 
                                Stock = Stock, common = COMMON, stock = current_stock)

    @app.route('/portfolio')
    def portfolio():
        global current_player
        return render_template ('portfolio.html', player = current_player, Player=Player, common = COMMON, 
                                Stock = Stock, stock = current_stock)

    @app.route('/ledger')
    def ledger():
        global current_player
    #     print ('from the ledger route', current_player.name)
        return render_template ('ledger.html', player = current_player, Player=Player, common = COMMON, 
                                Stock = Stock, stock = current_stock)

    @app.route('/graph')
    def plot():
        global current_stock
        png_output = BytesIO()
        
        #https://www.youtube.com/watch?v=6rKe2IEIu8c  Three are 2 ways of making plots
        figure1 = plt.figure(figsize=(12.5, 8))
                # adding the subplot
        plot1 = figure1.add_subplot(1,1,1) #num of plot, numb of columns, current plot
        legend_label = '{} Adj. Close Price History'.format (current_stock.symbol)  #https://www.youtube.com/watch?v=vTX3IwquFkc
        plot_data = current_stock.price_history(300)
        plt.plot(plot_data['adjclose'], label=legend_label)
        plt.plot(plot_data['SMA30'], label="30 day average", alpha = 0.35)
        plt.plot(plot_data['SMA100'], label="100 day average", alpha = 0.35)
        
        plt.scatter(plot_data.index, plot_data['Buy_Signal_Price'], label = 'BUY', marker = '^', color = 'green')
        plt.scatter(plot_data.index, plot_data['Sell_Signal_Price'], label = 'SELL', marker = 'v', color = 'red')
        plt.xlabel('Date')
        plt.ylabel('Adj. Close Price (USD)')
        plt.legend(loc='upper left')
        plot1.set_title('Stock history of ' +
                        str(current_stock.full_name()) +
                        " with a closing price of " +
                        str("${:,.2f}".format(current_stock.current_price())))
        plt.savefig(png_output, format='png')
        plt.close()
        png_output.seek(0)
        plot_url = base64.b64encode(png_output.getvalue()).decode('utf8')

        return render_template ('graph.html',
                                stock = current_stock,
                                Stock = Stock,
                                plot_url = plot_url,
                                player = current_player,
                                Player = Player,
                                common = COMMON)

if __name__ == "__main__":
    # execute only if run as a script
    main_loop()