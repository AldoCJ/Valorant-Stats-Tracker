

from fetch_data import *
from database_upload import *

def update_players():
    regions = ["na", "eu", "ap", "br", "jp", "oce", "mn", "cn", "kr"]

    for region in regions:
        if retrieve_players(region):
            upload_players("player_data.json", region)
            print (f"{region} players uploaded to the database!")
        else:
            print(f"Failed to retrieve {region} players.")

def update_matches():
    if retrieve_matches("upcoming"):
        upload_upcoming_matches("match_data.json")
        print (f"Upcoming matches uploaded to the database!")
    else:
        print(f"Failed to retrieve upcoming matches.")

    if retrieve_matches("results"):
        upload_match_results("match_data.json")
        print (f"Results matches uploaded to the database!")
    else:
        print(f"Failed to retrieve results matches.")

def update_teams():
    regions = ["na", "eu", "ap", "la", "la-s", "la-n", "oce", "kr", "mn", "br", "cn", "jp"]
    for region in regions:
        if retrieve_teams(region):
            upload_teams("team_data.json", region)
            print (f"{region} teams uploaded to the database!")
        else:
            print(f"Failed to retrieve {region} teams.")    

if __name__ == "__main__":
    update_players()
    update_teams()
    update_matches()


