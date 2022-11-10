import sqlite3 as sl
import json
import requests

def get_player_data():
    return json.loads((requests.get(f"https://api.sleeper.app/v1/players/nfl")).text)

con = sl.connect('players.db')
cursor = con.cursor()

create_cmd = "CREATE TABLE IF NOT EXISTS players (\
    player_id TEXT PRIMARY KEY, \
    number INTEGER, \
    weight TEXT, \
    position TEXT, \
    team TEXT, \
    last_name TEXT, \
    college TEXT, \
    age INTEGER, \
    height INTEGER, \
    stats_id TEXT, \
    birth_country TEXT, \
    first_name TEXT, \
    years_exp INTEGER\
    );"

cursor.execute(create_cmd)
traffic = get_player_data()
columns = [
    'player_id',
    'number',
    'weight',
    'position',
    'team',
    'last_name',
    'college',
    'age',
    'height',
    'stats_id',
    'birth_country',
    'first_name',
    'years_exp',
]

player_count = 0
for player in traffic:
    items = traffic[player]
    if(items['position'] != 'DEF'):
        keys = tuple(items[c] for c in columns)
        cursor.execute('INSERT INTO players values(?,?,?,?,?,?,?,?,?,?,?,?,?)', keys)
        player_count+= 1
        if(player_count % 50 == 0):
            print(f'count: {player_count}, recent addition: {items["first_name"]} {items["last_name"]}')

con.commit()
con.close()