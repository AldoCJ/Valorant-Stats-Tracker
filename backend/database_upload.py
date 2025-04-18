import mysql.connector
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re

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



teams = {
        "Team Vitality", 
        "Team Liquid", 
        "Team Heretics", 
        "FUT Esports", 
        "FNATIC", 
        "BBL Esports", 
        "Gentle Mates", 
        "GIANTX",  
        "KOI", 
        "Natus Vincere", 
        "Karmine Corp", 
        "Apeks", 
        "DRX", 
        "T1",  
        "Gen.G", 
        "TALON", 
        "Nongshim Redforce", 
        "DetonatioN FocusMe", 
        "Rex Regum Qeon", 
        "Paper Rex", 
        "BOOM Esports", 
        "Team Secret", 
        "Global Esports", 
        "ZETA DIVISION", 
        "G2 Esports", 
        "Sentinels",  
        "MIBR", 
        "KR\u00dc Esp",  
        "LEVIAT\u00c1N", 
        "LOUD", 
        "Evil Geniuses", 
        "NRG Esports",  
        "FURIA", 
        "Cloud9", 
        "100 Thieves", 
        "2Game Esports", 
        "EDward Gaming", 
        "Trace Esports", 
        "Bilibili Gaming", 
        "Dragon Ranger Gaming", 
        "FunPlus Phoenix",  
        "Xi Lai Gaming", 
        "Nova Esports", 
        "JDG Esports", 
        "Wolves Esports", 
        "TYLOO", 
        "Titan Esports Club", 
        "All Gamers" 
        }

player_teams = {
        "VIT", 
        "TL",  
        "TH", 
        "FUT", 
        "FNC", 
        "BBL", 
        "M8", 
        "GX", 
        "MKOI", 
        "NAVI", 
        "KC", 
        "APK", 
        "DRX", 
        "T1", 
        "GEN", 
        "TLN", 
        "NS", 
        "DFM", 
        "RRQ", 
        "PRX", 
        "BME", 
        "TS", 
        "GE", 
        "ZETA", 
        "G2", 
        "SEN", 
        "MIBR", 
        "KRÜ", 
        "LEV", 
        "LOUD", 
        "EG", 
        "NRG", 
        "FUR", 
        "C9", 
        "100T", 
        "2G", 
        "EDG", 
        "TE", 
        "BLG", 
        "DRG", 
        "FPX", 
        "XLG", 
        "NOVA", 
        "JDG", 
        "WOL", 
        "TYL", 
        "TEC", 
        "AG" 
        }

# Load environment variables
load_dotenv()

# Get database credentials from .env file
DB_HOST = os.getenv("HOST", "metro.proxy.rlwy.net")
DB_USER = os.getenv("USER", "root")
DB_PASSWORD = os.getenv("PASSWORD", "")
DB_NAME = os.getenv("NAME", "railway")
DB_PORT = os.getenv("PORT", "45442")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def upload_players(filename, region):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        with open(filename) as file:
            data = json.load(file)
            for player in data["data"]["segments"]:
                if player["org"] in player_teams:
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
                                float(player["rating"]), 
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
            print ("data uploaded")
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
                    cursor.execute(
                            """
                            INSERT IGNORE INTO upcoming_matches (team1, team2, flag1, flag2, series, event, time, page)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                team1 = VALUES(team1),
                                team2 = VALUES(team2),
                                flag1 = VALUES(flag1),
                                flag2 = VALUES(flag2),
                                series = VALUES(series),
                                event = VALUES(event),
                                time = VALUES(time),
                                page = VALUES(page)
                            """,
                            (
                                match["team1"], 
                                match["team2"], 
                                match["flag1"], 
                                match["flag2"], 
                                match["match_series"], 
                                match["match_event"], 
                                match["unix_timestamp"], 
                                match["match_page"]
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
                    cursor.execute(
                            """
                            INSERT IGNORE INTO recent_matches 
                            (team1, team2, score1, score2, flag1, flag2, round, tournament, time, page, tournament_icon)
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
                                match["match_page"],
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
        