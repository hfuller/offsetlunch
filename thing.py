from __future__ import print_function
import json
import psycopg2
import psycopg2.extras

from web_ui import WebUI

if __name__ == "__main__":
    print("Loading config file.")
    with open("config.json") as jconfig:
        config = json.load(jconfig)
    print("ok")
    
    db = psycopg2.connect(dbname=config['db']['name'], user=config['db']['user'], password=config['db']['password'])

    print("Starting WebUI")
    WebUI(db).go()

