from re import match
import requests
import json
import sqlite3
from enum import Enum

LEAGUE_ID = 859935711258902528

class Positions(Enum):
    QB = 'QB'
    RB = 'RB'
    WR = 'WR'
    TE = 'TE'

class Roster(Enum):
    QB = 'QB'
    RB1 = 'RB1'
    RB2 = 'RB2'
    WR1 = 'WR1'
    WR2 = 'WR2'
    TE = 'TE'
    FLEX1 = 'FLEX1'
    FLEX2 = 'FLEX2'
    SUPERFLEX = 'SUPERFLEX'

players_connection = sqlite3.connect("players.db")
players_cur = players_connection.cursor()


def get_matchups(league_id, week):
    response  = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}")
    return json.loads(response.text)

def optimize_lineup(players_points):
    default = 'NA'
    optimized_lineup = { Roster.QB.value : default, Roster.RB1.value : default, Roster.RB2.value : default, Roster.WR1.value : default, Roster.WR2.value : default, Roster.TE.value : default,
    Roster.FLEX1.value : default, Roster.FLEX2.value : default, Roster.SUPERFLEX.value : default }
    for player_item in players_points.items():
        player_id = player_item[0]
        player = { "id" : player_id, "points" : player_item[1], "position" : get_position(player_id) }
        if (player['position'] == Positions.QB.value):
            if (optimized_lineup[Roster.QB.value] == default or optimized_lineup[Roster.QB.value]['points'] < player['points']):
                swapped_player = optimized_lineup[Roster.QB.value]
                optimized_lineup[Roster.QB.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.SUPERFLEX.value] == default or optimized_lineup[Roster.SUPERFLEX.value]['points'] < player['points'])):
                optimized_lineup[Roster.SUPERFLEX.value] = player
        elif (player['position'] == Positions.RB.value):
            if (optimized_lineup[Roster.RB1.value] == default or optimized_lineup[Roster.RB1.value]['points'] < player['points']):
                swapped_player = optimized_lineup[Roster.RB1.value]
                optimized_lineup[Roster.RB1.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.RB2.value] == default or optimized_lineup[Roster.RB2.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.RB2.value]
                optimized_lineup[Roster.RB2.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX1.value] == default or optimized_lineup[Roster.FLEX1.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX1.value]
                optimized_lineup[Roster.FLEX1.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX2.value] == default or optimized_lineup[Roster.FLEX2.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX2.value]
                optimized_lineup[Roster.FLEX2.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.SUPERFLEX.value] == default or optimized_lineup[Roster.SUPERFLEX.value]['points'] < player['points'])):
                optimized_lineup[Roster.SUPERFLEX.value] = player
        elif (player['position'] == Positions.WR.value):
            if (optimized_lineup[Roster.WR1.value] == default or optimized_lineup[Roster.WR1.value]['points'] < player['points']):
                swapped_player = optimized_lineup[Roster.WR1.value]
                optimized_lineup[Roster.WR1.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.WR2.value] == default or optimized_lineup[Roster.WR2.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.WR2.value]
                optimized_lineup[Roster.WR2.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX1.value] == default or optimized_lineup[Roster.FLEX1.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX1.value]
                optimized_lineup[Roster.FLEX1.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX2.value] == default or optimized_lineup[Roster.FLEX2.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX2.value]
                optimized_lineup[Roster.FLEX2.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.SUPERFLEX.value] == default or optimized_lineup[Roster.SUPERFLEX.value]['points'] < player['points'])):
                optimized_lineup[Roster.SUPERFLEX.value] = player
        elif (player['position'] == Positions.TE.value):
            if (optimized_lineup[Roster.TE.value] == default or optimized_lineup[Roster.TE.value]['points'] < player['points']):
                swapped_player = optimized_lineup[Roster.TE.value]
                optimized_lineup[Roster.TE.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX1.value] == default or optimized_lineup[Roster.FLEX1.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX1.value]
                optimized_lineup[Roster.FLEX1.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.FLEX2.value] == default or optimized_lineup[Roster.FLEX2.value]['points'] < player['points'])):
                swapped_player = optimized_lineup[Roster.FLEX2.value]
                optimized_lineup[Roster.FLEX2.value] = player
                player = swapped_player
            if (player != default and (optimized_lineup[Roster.SUPERFLEX.value] == default or optimized_lineup[Roster.SUPERFLEX.value]['points'] < player['points'])):
                optimized_lineup[Roster.SUPERFLEX.value] = player
    return optimized_lineup

def get_optimized_lineup_score(players_points):
    score = 0
    for player in optimize_lineup(players_points).values():
        score+= player['points']
    return score

def get_position(player_id):
    return players_cur.execute(f"SELECT position FROM players WHERE player_id='{player_id}'").fetchone()[0]

def get_rosters(league_id):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/rosters")
    return json.loads(response.text)

def get_league_teams(league_id):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/users")
    teams = []
    for team in json.loads(response.text):
        teams.append({ 'user_id' : team['user_id'], 'display_name' : team['display_name'], 'team_name' : team['metadata'].get('team_name', f'Team {team["display_name"]}')})
    for roster in get_rosters(league_id):
        for team in teams:
            if (roster['owner_id'] == team['user_id']):
                team['roster_id'] = roster['roster_id']
    return teams

def get_optimized_records(league_id, last_week):
    teams = get_league_teams(league_id)
    for team in teams:
        team['wins'], team['losses'], team['ties'], team['optimized_total_points'] = 0, 0, 0, 0

    for cur_week in range(1, last_week + 1):
        print(f"calculating week {cur_week}")
        matchups = {}
        for team_performance in get_matchups(league_id, cur_week):
            for team in teams:
                if(team['roster_id'] == team_performance['roster_id']):
                    players_points = team_performance['players_points']
                    matchup_id = team_performance['matchup_id']
                    team_temp = team
                    team_temp['optimized_score'] = get_optimized_lineup_score(players_points)
                    if(matchups.get(matchup_id)):
                        matchups.get(matchup_id).append(team_temp)
                    else:
                        matchups[matchup_id] = [team_temp]
        for matchup in matchups.values():
            for team_one in teams:
                if team_one['roster_id'] == matchup[0]['roster_id']:
                    for team_two in teams:
                        if team_two['roster_id'] == matchup[1]['roster_id']:
                            team_one['optimized_total_points'] = team_one['optimized_total_points'] + team_one['optimized_score']
                            team_two['optimized_total_points'] = team_two['optimized_total_points'] + team_two['optimized_score']
                            if(team_one['optimized_score'] > team_two['optimized_score']):
                                team_one['wins'] = team_one['wins'] + 1
                                team_two['losses'] = team_two['losses'] + 1
                            elif(team_one['optimized_score'] < team_two['optimized_score']):
                                team_one['losses'] = team_one['losses'] + 1
                                team_two['wins'] = team_two['wins'] + 1
                            else:
                                team_one['ties'] = team_one['ties'] + 1
                                team_two['ties'] = team_two['ties'] + 1
    return teams

def print_standings(teams):
    rank = 1
    print()
    print('based on record')
    for team in sorted(teams, key=lambda x: (x['wins'], x['optimized_total_points']), reverse=False):
        print(f"{rank}. {team['team_name']} ({team['wins']}, {team['losses']}) PF: {round(team['optimized_total_points'], 2)}")
        rank+= 1
    rank = 1
    print()
    print('based on points scored')
    for team in sorted(teams, key=lambda x: (x['optimized_total_points']), reverse=False):
        print(f"{rank}. {team['team_name']} ({team['wins']}, {team['losses']}) PF: {round(team['optimized_total_points'], 2)}")
        rank+= 1

print_standings(get_optimized_records(LEAGUE_ID, 13))

def get_league_profile_pics(league_id):
    response = requests.get(f"https://api.sleeper.app/v1/league/{league_id}/users")
    avatars = []
    for team in json.loads(response.text):
        avatars.append(team['avatar'])
    
    print(avatars)
    for avatar in avatars:
        response = requests.get(f"https://sleepercdn.com/avatars/{avatar}")
        with open(f"C://Users//guill//OneDrive//Documents//fantasy football//avatars//{avatar}.png", 'wb') as f:
            f.write(response.content)

players_connection.commit()
players_connection.close()
