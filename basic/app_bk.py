from flask import Flask, render_template, request

import datetime
from db_data import *
from ST_classes_NEW import *
import pdb

app = Flask(__name__)
player_id = ""
current_player = 'Michael'

@app.route('/')
@app.route('/<player_id>')
def index(player_id = 'Michael'):
    global current_player
    title = "This is web based STOCK TICKER"
    current_player = player_id
    print ('from the index route', current_player, "   ", player_id)
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
    return render_template ('about.html')

@app.route('/index_test')
def index_test():
    global current_player
    title = "This is a test page"
    return render_template ('index_test.html', title = title, player = current_player, Player=Player)

@app.route('/newplayer')
def newplayer():
    return render_template ('newplayer.html')

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
    print ('from the ledger route', current_player)
    return render_template ('ledger.html', player = current_player, Player=Player)