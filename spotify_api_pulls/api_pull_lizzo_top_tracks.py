#Pull a Spotify artists top tracks and analyze that data
import requests
import json
import argparse

#set up args for api_key so it's not included in code for security
#can also set up env variables, but spotify api keys expire
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--api_key", required=True, help="Api key for OAuth")
parser.add_argument("-i", "--id", required=True, help="Spotify artist ID")
args = parser.parse_args()

api_key=args.api_key
artist_id=args.id

#set up required headers for spotify artist's top tracks API
#https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer %s" % api_key}

#future enhancement can be to allow user to enter an artist's name and then look up the ID
response = requests.get("https://api.spotify.com/v1/artists/%s/top-tracks?country=US" % artist_id, headers=headers, verify=False)
request = json.loads(response.text)
tracks = request["tracks"]
# tracks = response.text

#pretty print the json data into an outputted text file
#tracks_data = open("tracks_data.json", 'w+')
#tracks_data.write(json.dumps(tracks, indent = 4, sort_keys=True))
#print(json.dumps(tracks, indent = 4, sort_keys=True))

print(type(tracks))

for item in tracks:
    print(item["name"])
    print(item["popularity"])