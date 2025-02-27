# Here we will define the structure of our database and the functions that interact with it.

from fetch_data import *
from database_upload import *

def update_players():
    regions = ["na", "eu", "ap", "sa"]

    for region in regions:
        if retreive_players(region):
            upload_players("player_data.json", region)
            print (f"{region} players uploaded to the database!")
        else:
            print(f"Failed to retrieve {region} players.")

def update_matches():
    parameters = ['upcoming', 'live_score', 'results']
    for parameter in parameters:
        if retreive_matches(parameter):
            print (f"{parameter} matches uploaded to the database!")
        else:
            print(f"Failed to retrieve {parameter} matches.")

def update_teams():
    regions = ["na", "eu", "ap", "sa"]
    for region in regions:
        if retrieve_teams(region):
            upload_teams("team_data.json", region)
            print (f"{region} teams uploaded to the database!")
        else:
            print(f"Failed to retrieve {region} teams.")    


