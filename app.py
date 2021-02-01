from flask import Flask, render_template, request, make_response

import datetime
from db_data import *
from ST_classes_NEW import *

from io import BytesIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

app = Flask(__name__)

@app.route('/')
def main():
    global current_player, current_stock
    title = "This is web based STOCK TICKER"
    player_id = request.args.get("name", "Michael") #Michael is the default   127.0.0.1:5000/?name=michael
    stock_symb = request.args.get("stock", "aapl") #aapl is the default   127.0.0.1:5000/?stock=aapl
    current_player = Player(player_id)
#     print ('from the MAIN route', current_player.name, "   ", player_id)
    common = [("amzn", "Amazon.com, Inc."),
             ("goog", "Alphabet Inc Class C"),
             ("aapl", "Apple Inc"),
             ("tsla", "Tesla Inc"),
             ("coke", "Coca-Cola Consolidated Inc"),
             ("ba", "Boeing Co"),
             ("su", "Suncor Energy Inc."),
             ("f", "Ford"),
             ("msft", "Microsoft"),
             ("mar", "Marriott International"),
             ("nflx", "Netflix Inc"),
             ("ac", "Air Canada"),
             ("fb", "Facebook, Inc. Common Stock"),
             ("zm", "Zoom Video Com")
             ]
    return render_template ('index.html', title = title, common = common, player = current_player, Player=Player)

@app.route('/about')
def about():
    global current_player
    return render_template ('about.html')

@app.route('/newplayer')
def newplayer():
    return render_template ('newplayer.html', player = current_player, Player=Player)

@app.route('/form', methods=["POST"])
def form():
    global current_player
    name = request.form.get ("name")
    current_player = Player (name)
    return render_template ('form.html', player = current_player, Player=Player)

@app.route('/networth')
def networth():
    global current_player
    return render_template ('networth.html', player = current_player, Player=Player)

@app.route('/portfolio')
def portfolio():
    global current_player
    return render_template ('portfolio.html', player = current_player, Player=Player)

@app.route('/ledger')
def ledger():
    global current_player
#     print ('from the ledger route', current_player.name)
    return render_template ('ledger.html', player = current_player, Player=Player)

@app.route("/simple.png")
def simple():
    stock = Stock(symbol)
    self.current_stock = stock
    figure1 = plt.figure(figsize=(12.5, 8))
            # adding the subplot
    plot1 = figure1.add_subplot(111)
    canvas=FigureCanvas(fig)
    plt.plot(stock.price_history()['adjclose'], label=symbol)
    plt.title('Adj. Close Price History')
    plt.xlabel('Date')
    plt.ylabel('Adj. Close Price (USD)')
    plt.legend(loc='upper left')
    plot1.set_title('Stock history of ' +
                    str(stock.full_name()) +
                    " with a closing price of " +
                    str("${:,.2f}".format(stock.current_price())))
    
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response