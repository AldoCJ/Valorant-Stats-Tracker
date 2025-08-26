# This is where create functions that will make requests to the vlrggapi to retrieve data
# and then store that data in the database.

import requests
import json

def retrieve_players(region):
    url = f"https://vlrggapi.vercel.app/stats?region={region}&timespan=90"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        with open("player_data.json", "w") as file:
            json.dump(data, file, indent=4)
        return True
    else:
        print(f"Error: {response.status_code}")
        return False
    
def retrieve_matches(parameter):
    
    url = f"https://vlrggapi.vercel.app/match?q={parameter}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        with open("match_data.json", "w") as file:
            json.dump(data, file, indent=4)
        return True
    else:
        print(f"Error: {response.status_code}")
        return False
    
def retrieve_teams(region):
    url = f"https://vlrggapi.vercel.app/rankings?region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        with open("team_data.json", "w") as file:
            json.dump(data, file, indent=4)
        return True
    else:
        print(f"Error: {response.status_code}")
        return False
    