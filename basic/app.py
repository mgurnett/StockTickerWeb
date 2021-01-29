from flask import Flask, render_template, request

import datetime
from db_data import *
from ST_classes_NEW import *

app = Flask(__name__)
player_id = 'Michael'

@app.route('/')
def main():
    title = "This is web based STOCK TICKER"
    player_id = 'Michael'
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

@app.route('/<player_id>')
def index(player_id):
#     player_id = 'Michael'
    title = "This is web based STOCK TICKER"
    current_player = Player(player_id)
    print ('from the INDEX route', current_player.name, "   ", player_id)
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

@app.route('/ledger')
def ledger():
    
    current_player = Player(player_id)
    print ('from the ledger route', current_player.name)
    return render_template ('ledger.html', player = current_player, Player=Player)