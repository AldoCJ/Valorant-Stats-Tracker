import json
from datetime import datetime, timedelta
import re
from teams import *
from connection import *
from match_predictor import *


def get_event_time(time_str):
    """
    Takes a string like "3h 45m ago" and returns the datetime of the event.
    """
    # Current time
    now = datetime.now()

    # Extract hours and minutes using regex
    match = re.search(r'(?:(\d+)h)?\s*(?:(\d+)m)?\s*ago', time_str)
    if not match:
        raise ValueError("Time string is not in the correct format")

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0

    # Subtract the time delta
    event_time = now - timedelta(hours=hours, minutes=minutes)
    return event_time

def upload_players(filename, region):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open(filename) as file:
            data = json.load(file)
            for player in data["data"]["segments"]:
                if player["org"] in player_teams:
                    for agent in player["agents"]:
                        cursor.execute(
                            """
                            INSERT IGNORE INTO agents_played (player, agent_name)
                            VALUES(%s, %s)
                            """,
                            (player["player"], agent)   
                        )
                    rating_str = player["rating"].strip()
                    rating = float(rating_str) if rating_str else None
                    cursor.execute(
                            """
                            INSERT INTO players (player, org, rounds_played, rating, average_combat_score, kill_deaths, kill_assists_survived_traded,
                            average_damage_per_round, kills_per_round, assists_per_round, first_kills_per_round, first_deaths_per_round,
                            headshot_percentage, clutch_success_percentage, region)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                org = VALUES(org),
                                rounds_played = VALUES(rounds_played),
                                rating = VALUES(rating),
                                average_combat_score = VALUES(average_combat_score),
                                kill_deaths = VALUES(kill_deaths),
                                kill_assists_survived_traded = VALUES(kill_assists_survived_traded),
                                average_damage_per_round = VALUES(average_damage_per_round),
                                kills_per_round = VALUES(kills_per_round),
                                assists_per_round = VALUES(assists_per_round),
                                first_kills_per_round = VALUES(first_kills_per_round),
                                first_deaths_per_round = VALUES(first_deaths_per_round),
                                headshot_percentage = VALUES(headshot_percentage),
                                clutch_success_percentage = VALUES(clutch_success_percentage),
                                region = VALUES(region)
                            """,
                            
                            (
                                player["player"], 
                                player["org"], 
                                int(player["rounds_played"]), 
                                rating, 
                                float(player["average_combat_score"]),
                                float(player["kill_deaths"]),
                                player["kill_assists_survived_traded"], 
                                float(player["average_damage_per_round"]), 
                                float(player["kills_per_round"]), 
                                float(player["assists_per_round"]), 
                                float(player["first_kills_per_round"]), 
                                float(player["first_deaths_per_round"]), 
                                player["headshot_percentage"],
                                player["clutch_success_percentage"],
                                region
                            )
                    )
        conn.commit()
        cursor.close()
        conn.close()

def upload_upcoming_matches(filename):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open(filename) as file:
            data = json.load(file)
            for match in data["data"]["segments"]:
                if "Champions Tour" in match["match_event"]: 
                    prediction_data = extract_prediction_data(match)
                    if prediction_data:
                        team1_pred, team2_pred = predict_winner(prediction_data)
                    else:
                        team1_pred = None
                        team2_pred = None
                    cursor.execute(
                            """
                            INSERT IGNORE INTO upcoming_matches (team1, team2, flag1, flag2, series, event, time, page,
                             team1_pred, team2_pred)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                match["team1"], 
                                match["team2"], 
                                match["flag1"], 
                                match["flag2"], 
                                match["match_series"], 
                                match["match_event"], 
                                match["unix_timestamp"], 
                                match["match_page"],
                                team1_pred,
                                team2_pred
                            )
                        )
            cursor.execute(
                    """
                    DELETE FROM upcoming_matches
                    WHERE time < NOW();
                    """
                    )
           
        print ("data uploaded")
        conn.commit()
        cursor.close()
        conn.close()

def upload_match_results(filename):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open(filename) as file:
            data = json.load(file)
            for match in data["data"]["segments"]:
                if "Champions Tour" in match["tournament_name"]: 
                    page = "https://www.vlr.gg" + match["match_page"]
                    cursor.execute(
                            """
                            INSERT IGNORE INTO recent_matches 
                            (team1, team2, score1, score2, flag1, flag2, series, event, time, page, tournament_icon)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                match["team1"], 
                                match["team2"], 
                                match["score1"], 
                                match["score2"], 
                                match["flag1"], 
                                match["flag2"],
                                match["round_info"],
                                match["tournament_name"],
                                get_event_time(match["time_completed"]), 
                                page,
                                match["tournament_icon"]
                            )
                    )
        print ("data uploaded")
        conn.commit()
        cursor.close()
        conn.close()

def upload_teams(filename, region):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        
        with open(filename) as file:
            data = json.load(file)
            for team in data["data"]:
                if team["team"] in teams:
                    cursor.execute(
                            """
                            INSERT INTO teams (ranking, team, country, last_played, last_played_team, last_played_team_logo,
                            record, earnings, logo, region)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                ranking = VALUES(ranking),
                                team = VALUES(team),
                                country = VALUES(country),
                                last_played = VALUES(last_played),
                                last_played_team = VALUES(last_played_team),
                                last_played_team_logo = VALUES(last_played_team_logo),
                                record = VALUES(record),
                                earnings = VALUES(earnings),
                                logo = VALUES(logo),
                                region = VALUES(region)
                            """,
                            (
                                team["rank"],
                                team["team"],
                                team["country"],
                                team["last_played"],
                                team["last_played_team"],
                                team["last_played_team_logo"],
                                team["record"],
                                team["earnings"],
                                team["logo"],
                                region
                            )
                    )
        print ("data uploaded")
        conn.commit()
        cursor.close()
        conn.close()
        