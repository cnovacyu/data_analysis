import sys
import spotipy
import spotipy.util as util

export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username)

lizzo_uri = 'spotify:artist:56oDRnqbIiwx4mymNEv7dS'

if token:
    spotify = spotipy.Spotify(auth=token)
    results = spotify.artist_albums(lizzo_uri, album_type='album')
    albums = results['items']

    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])
else:
    print("Can't get token for", username)