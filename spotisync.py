import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import pandas as pd
import sys
import time
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

# YouTube authentication (lazy loading)
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
youtube = None

def get_youtube_client():
    """Lazy load YouTube client only when needed"""
    global youtube
    if youtube is None:
        try:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_OAUTH_FILE, scopes)
            credentials = flow.run_local_server(port=8080)
            youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
        except Exception as e:
            print(f"❌ Error authenticating with YouTube: {e}")
            sys.exit(1)
    return youtube

# List Spotify playlists (with pagination)
def list_playlists():
    try:
        all_playlists = []
        offset = 0
        limit = 50

        while True:
            playlists = sp.current_user_playlists(limit=limit, offset=offset)
            all_playlists.extend(playlists['items'])

            if playlists['next'] is None:
                break
            offset += limit

        print("\n📋 **Available Spotify Playlists:**\n")
        for index, playlist in enumerate(all_playlists):
            print(f"[{index}] {playlist['name']} - {playlist['id']}")

        return all_playlists
    except Exception as e:
        print(f"❌ Error listing playlists: {e}")
        return []

# Get tracks from a Spotify playlist (with pagination)
def get_playlist_tracks(playlist_id):
    try:
        tracks = []
        offset = 0
        limit = 100

        while True:
            results = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
            for item in results['items']:
                if item['track'] and item['track']['name']:
                    track = item['track']
                    artist = track["artists"][0]["name"] if track["artists"] else "Unknown Artist"
                    tracks.append({"name": track["name"], "artist": artist})

            if results['next'] is None:
                break
            offset += limit

        return tracks
    except Exception as e:
        print(f"❌ Error getting playlist tracks: {e}")
        return []

# List YouTube playlists (with pagination)
def get_youtube_playlists():
    try:
        yt = get_youtube_client()
        playlists = {}
        next_page_token = None

        while True:
            request = yt.playlists().list(
                part="snippet",
                mine=True,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get("items", []):
                playlists[item["snippet"]["title"]] = item["id"]

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return playlists
    except Exception as e:
        print(f"❌ Error listing YouTube playlists: {e}")
        return {}

# Delete a YouTube playlist
def delete_youtube_playlist(playlist_id):
    try:
        yt = get_youtube_client()
        request = yt.playlists().delete(id=playlist_id)
        request.execute()
    except Exception as e:
        print(f"❌ Error deleting YouTube playlist: {e}")

# Create a new YouTube playlist
def create_youtube_playlist(name):
    try:
        yt = get_youtube_client()
        request = yt.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {"title": name, "description": "Imported from Spotify"},
                "status": {"privacyStatus": "private"}
            }
        )
        response = request.execute()
        return response["id"]
    except Exception as e:
        print(f"❌ Error creating YouTube playlist: {e}")
        return None

# Search for a track on YouTube
def search_youtube_track(song_name, artist):
    try:
        yt = get_youtube_client()
        query = f"{song_name} {artist} official"
        request = yt.search().list(part="snippet", maxResults=1, q=query, type="video")
        response = request.execute()

        if "items" in response and response["items"]:
            return response["items"][0]["id"]["videoId"]
        return None
    except Exception as e:
        print(f"⚠️ Error searching for '{song_name}' by {artist}: {e}")
        return None

# Add a video to a YouTube playlist
def add_video_to_playlist(playlist_id, video_id):
    """Add a video to a YouTube playlist with rate limiting"""
    try:
        yt = get_youtube_client()
        request = yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
        time.sleep(0.1)  # Rate limiting: 100ms delay between additions
        return True
    except Exception as e:
        print(f"⚠️ Error adding video {video_id} to playlist: {e}")
        return False

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
    try:
        # Create logs directory if it doesn't exist
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)

        # Save to logs directory
        filepath = os.path.join(logs_dir, filename)
        df = pd.DataFrame(log_tracks)
        df.to_csv(filepath, index=False, encoding="utf-8")
        print(f"✅ Log saved as {filepath}")
    except Exception as e:
        print(f"❌ Error saving log: {e}")

# Display a table of results
def display_log_table(log_tracks):
    """Display import results in a formatted table"""
    if not log_tracks:
        print("\n⚠️ No tracks to display")
        return

    print("\n" + "="*60)
    print(f"{'Title':<40} {'Artist':<25} {'Status':<15}")
    print("="*60)

    for track in log_tracks:
        title = track['Title'][:37] + "..." if len(track['Title']) > 40 else track['Title']
        artist = track['Artist'][:22] + "..." if len(track['Artist']) > 25 else track['Artist']
        status = track['Status']
        status_icon = "✅" if status == "Added" else "❌"

        print(f"{title:<40} {artist:<25} {status_icon} {status:<13}")

    print("="*60)

    # Summary
    added = sum(1 for t in log_tracks if t['Status'] == 'Added')
    not_found = len(log_tracks) - added
    print(f"\n📊 Summary: {added} added, {not_found} not found (Total: {len(log_tracks)})\n")

# Console interface
def main():
    playlists_cache = None  # Cache for playlists to avoid repeated API calls

    while True:
        print("\n🟢 **Available Commands:**")
        print("   list                     → Show Spotify playlists")
        print("   export_youtube <number>  → Export a playlist to YouTube Music")
        print("   exit                     → Quit\n")

        command = input("👉 Command: ").strip()

        if command == "list":
            playlists_cache = list_playlists()

        elif command.startswith("export_youtube"):
            parts = command.split()
            if len(parts) < 2:
                print("❌ Invalid format! Use: export_youtube <number>")
                continue

            try:
                playlist_index = int(parts[1])

                # Load playlists if not cached
                if playlists_cache is None:
                    print("📋 Loading playlists...")
                    playlists_cache = list_playlists()

                if playlist_index >= len(playlists_cache) or playlist_index < 0:
                    print("❌ Invalid playlist number.")
                    continue

                playlist_id = playlists_cache[playlist_index]["id"]
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