# This is where create functions that will make requests to the vlrggapi to retrieve data
# and then store that data in the database.

import requests
import json

url = "https://vlrggapi.vercel.app/stats?region=na&timespan=30"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    with open("matches_data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Data fetched successfully")
else:
    print(f"Error: {response.status_code}")