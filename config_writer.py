from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["DATABASE"] = {
    "db_file_name" : "stock_ticker.db",
    "DEBUG" : True
}

config_object ["COLOURS"] = {
    "frame_color" : "#34568b",
    "message_color" : "BlanchedAlmond",
    "canvas_color" : "#8faad6",
    "root_color" : "#5780c1"
}

config_object ["PLAYERS"] = {
    "initial" : 10000
    }

#Write the above sections to config.ini file
with open('ST_config.ini', 'w') as conf:
    config_object.write(conf)