from flask import Flask, render_template, request

import datetime
from db_data import *
from ST_classes_NEW import *

app = Flask(__name__)

@app.route('/')
def main():
    global player_id
    title = "This is web based STOCK TICKER"
    player_id = request.args.get("name", "Michael") #Michael is the default   127.0.0.1:5000/?name=michael
    current_player = Player(player_id)
    print ('from the MAIN route', current_player.name, "   ", player_id)
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
    current_player = "Michael"
    return render_template ('about.html')

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
    global player_id
    print ('from the ledger route player_id', player_id)
    current_player = Player(player_id)
    print ('from the ledger route', current_player.name, "   ", player_id)
    return render_template ('ledger.html', player = current_player, Player=Player)