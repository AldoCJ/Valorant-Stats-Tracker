import json
from connection import *
from teams import *
import re
import decimal

def win_loss_ratio(record_str):
    match = re.match(r"(\d+)\D+(\d+)", record_str)
    if match:
        wins, losses = map(int, match.groups())
        return wins / (wins + losses) if (wins + losses) > 0 else 0
    return 0  # fallback if pattern doesn't match

def convert_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def extract_prediction_data(match):
    team1 = match["team1"]
    team2 = match["team2"]
    team1_abbr = team_name_to_abbreviation.get(team1)
    team2_abbr = team_name_to_abbreviation.get(team2)

    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        # Fetch player data for team1
        query = "SELECT rating, average_combat_score, kill_deaths," \
        " kill_assists_survived_traded, average_damage_per_round, kills_per_round, assists_per_round," \
        " first_kills_per_round, first_deaths_per_round, headshot_percentage, clutch_success_percentage FROM players WHERE org = %s"

        cursor.execute(query, (team1_abbr,))
        team1_players = cursor.fetchall()

        # Fetch player data for team2
        cursor.execute(query, (team2_abbr,))
        team2_players = cursor.fetchall()

        # Fetch team data for win/loss ratios
        query = "SELECT record FROM teams WHERE team = %s"

        cursor.execute(query, (team1,))
        team1_win_loss = cursor.fetchone()
        team1_win_loss = win_loss_ratio(team1_win_loss["record"]) if team1_win_loss else 0  # Fallback to 0 if no record

        cursor.execute(query, (team2,))
        team2_win_loss = cursor.fetchone()
        team2_win_loss = win_loss_ratio(team2_win_loss["record"]) if team2_win_loss else 0  # Fallback to 0 if no record

        # Handle missing player data for team1
        if not team1_players:
            print(f"Warning: No player data found for {team1}. Using default player stats.")
            team1_players = [{
                "rating": 0.99,
                "average_combat_score": 195.0,
                "kill_deaths": 0.99,
                "kill_assists_survived_traded": "69%",
                "average_damage_per_round": 128.0,
                "kills_per_round": 0.68,
                "assists_per_round": 0.28,
                "first_kills_per_round": 0.09,
                "first_deaths_per_round": 0.09,
                "headshot_percentage": "27%",
                "clutch_success_percentage": "12%"
            }]
        
        # Handle missing player data for team2 
        if not team2_players:
            print(f"Warning: No player data found for {team2}. Using default player stats.")
            team2_players = [{
                "rating": 0.99,
                "average_combat_score": 195.0,
                "kill_deaths": 0.99,
                "kill_assists_survived_traded": "69%",
                "average_damage_per_round": 128.0,
                "kills_per_round": 0.68,
                "assists_per_round": 0.28,
                "first_kills_per_round": 0.09,
                "first_deaths_per_round": 0.09,
                "headshot_percentage": "27%",
                "clutch_success_percentage": "12%"
            }]
        
        # Prepare the final data
        data = {
            "team1": {
                "win/loss": team1_win_loss,
                "player_stats": team1_players
            },
            "team2": {
                "win/loss": team2_win_loss,
                "player_stats": team2_players
            }
        }

        cursor.close()
        conn.close()

        return data
    
    return None  # Return None if connection fails


def predict_winner(data):
    team1_stats_list = data["team1"]["player_stats"]
    team2_stats_list = data["team2"]["player_stats"]

    # Handle missing player stats
    if not team1_stats_list or not team2_stats_list:
        return (50, 50)

    def clean_percentage(val):
        if isinstance(val, str) and "%" in val:
            return float(val.strip("%")) / 100
        try:
            return float(val)
        except:
            return 0.0

    # Compute average for each team
    def average_team_stats(players):
        stat_sums = {}
        count = len(players)

        for player in players:
            for key, val in player.items():
                val = clean_percentage(val)
                stat_sums[key] = stat_sums.get(key, 0) + val

        return {k: v / count for k, v in stat_sums.items()}

    team1_stats = average_team_stats(team1_stats_list)
    team2_stats = average_team_stats(team2_stats_list)

    team1_score = data["team1"]["win/loss"]
    team2_score = data["team2"]["win/loss"]

    # Scale down these large values
    max_expected = {
        "average_combat_score": 300,
        "average_damage_per_round": 200,
    }

    for key in team1_stats:
        t1 = team1_stats[key]
        t2 = team2_stats.get(key, 0)

        # Normalize large stats
        if key in max_expected:
            t1 /= max_expected[key]
            t2 /= max_expected[key]

        if t1 > t2:
            team1_score += 1
        elif t2 > t1:
            team2_score += 1

    total = team1_score + team2_score
    team1_percent = round((team1_score / total) * 100)
    team2_percent = 100 - team1_percent

    return (team1_percent, team2_percent)
