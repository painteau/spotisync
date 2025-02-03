import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import pandas as pd
import ace_tools as ace  # For displaying a table
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve credentials from .env file
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
YOUTUBE_OAUTH_FILE = os.getenv("YOUTUBE_OAUTH_FILE")

# Check if all required variables are set
if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, YOUTUBE_OAUTH_FILE]):
    print("❌ Error: Missing required variables in .env file.")
    sys.exit(1)

# Authenticate Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-read-private"))

# Authenticate YouTube
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        YOUTUBE_OAUTH_FILE, scopes)
    credentials = flow.run_local_server(port=8080)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

youtube = authenticate_youtube()

# List Spotify playlists
def list_playlists():
    playlists = sp.current_user_playlists()
    print("\n📋 **Available Spotify Playlists:**\n")
    for index, playlist in enumerate(playlists['items']):
        print(f"[{index}] {playlist['name']} - {playlist['id']}")

# Get tracks from a Spotify playlist
def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    for item in results['items']:
        track = item['track']
        tracks.append({"name": track["name"], "artist": track["artists"][0]["name"]})
    return tracks

# List YouTube playlists
def get_youtube_playlists():
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    response = request.execute()
    playlists = {}
    for item in response.get("items", []):
        playlists[item["snippet"]["title"]] = item["id"]
    return playlists

# Delete a YouTube playlist
def delete_youtube_playlist(playlist_id):
    request = youtube.playlists().delete(id=playlist_id)
    request.execute()

# Create a new YouTube playlist
def create_youtube_playlist(name):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": name, "description": "Imported from Spotify"},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]

# Search for a track on YouTube
def search_youtube_track(song_name, artist):
    query = f"{song_name} {artist} official"
    request = youtube.search().list(part="snippet", maxResults=1, q=query, type="video")
    response = request.execute()
    
    if "items" in response and response["items"]:
        return response["items"][0]["id"]["videoId"]
    return None

# Handle playlist conflicts on YouTube
def get_or_create_youtube_playlist(playlist_name):
    youtube_playlists = get_youtube_playlists()
    
    if playlist_name in youtube_playlists:
        print(f"\n⚠️ A YouTube playlist named **{playlist_name}** already exists.")
        choice = input("👉 Do you want to overwrite (delete and recreate) or create a new one? [o/n] ").strip().lower()

        if choice == "o":
            print(f"🚨 Deleting existing playlist: {playlist_name}")
            delete_youtube_playlist(youtube_playlists[playlist_name])
            print("✅ Creating a new playlist...")
            return create_youtube_playlist(playlist_name)
        else:
            print("📌 Creating a new playlist...")
    
    return create_youtube_playlist(playlist_name)

# Transfer Spotify playlist to YouTube Music
def migrate_spotify_to_youtube(playlist_id):
    # Retrieve Spotify playlist name
    playlist_info = sp.playlist(playlist_id)
    playlist_name = playlist_info["name"]

    print(f"\n🎵 Transferring playlist: {playlist_name}\n")

    tracks = get_playlist_tracks(playlist_id)
    youtube_playlist_id = get_or_create_youtube_playlist(playlist_name)

    if not youtube_playlist_id:
        print("❌ Error: Unable to create or retrieve YouTube playlist.")
        return

    log_tracks = []  # Store results

    for track in tracks:
        video_id = search_youtube_track(track["name"], track["artist"])
        status = "Added" if video_id else "Not found"
        
        if video_id:
            add_video_to_playlist(youtube_playlist_id, video_id)

        log_tracks.append({
            "Title": track["name"],
            "Artist": track["artist"],
            "Status": status
        })

    # Export log to CSV
    filename = f"{playlist_id}.csv"
    export_log_to_csv(log_tracks, filename)

    # Display results in a table
    display_log_table(log_tracks)

# Export log to CSV
def export_log_to_csv(log_tracks, filename):
    df = pd.DataFrame(log_tracks)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✅ Log saved as {filename}")

# Display a table of results
def display_log_table(log_tracks):
    df = pd.DataFrame(log_tracks)
    ace.display_dataframe_to_user(name="Import Results", dataframe=df)

# Console interface
def main():
    while True:
        print("\n🟢 **Available Commands:**")
        print("   list                     → Show Spotify playlists")
        print("   export_youtube <number>  → Export a playlist to YouTube Music")
        print("   exit                     → Quit\n")

        command = input("👉 Command: ").strip()

        if command == "list":
            list_playlists()
        
        elif command.startswith("export_youtube"):
            parts = command.split()
            if len(parts) < 2:
                print("❌ Invalid format! Use: export_youtube <number>")
                continue

            try:
                playlist_index = int(parts[1])
                playlists = sp.current_user_playlists()
                if playlist_index >= len(playlists["items"]):
                    print("❌ Invalid playlist number.")
                    continue

                playlist_id = playlists["items"][playlist_index]["id"]
                migrate_spotify_to_youtube(playlist_id)
            except ValueError:
                print("❌ The playlist number must be an integer.")

        elif command == "exit":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Unknown command.")

# Run the console interface
if __name__ == "__main__":
    main()