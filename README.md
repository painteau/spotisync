# 🎵 SpotiSync - Spotify to YouTube Music Playlist Converter

SpotiSync is a **Python-based CLI tool** that exports playlists from **Spotify** and imports them into **YouTube Music**.  
This project is fully containerized on **GitHub Container Registry (GHCR)**.

---

## 📌 Features
- 🔍 **Browse & List**: View all your **Spotify playlists** directly from the CLI.
- 🔄 **Playlist Transfer**: Export a **Spotify playlist** to **YouTube Music** seamlessly.
- 🎵 **Name Consistency**: Maintain the **same playlist name** across both platforms.
- ⚡ **Conflict Handling**:
  - **Overwrite Mode**: Delete and recreate existing playlists.
  - **Duplicate Mode**: Create a new playlist with a different name.
- 📊 **Export Logs**: Generate detailed **CSV logs** for every transferred playlist.
- 🛠️ **Automation**: Integrated **GitHub Actions** for automated **Docker builds** and updates.

---

## 🛠 Setup & Installation

### **1️⃣ Get Your API Keys**
#### **Spotify API Keys**
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create a **new application**.
3. Obtain your **Client ID** and **Client Secret**.
4. Set a **Redirect URI**:  
   ```
   http://localhost:8888/callback
   ```

#### **Google OAuth for YouTube**
1. Open the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create an **OAuth 2.0 Client ID**.
3. Choose **”Desktop App”**.
4. Download the `client_secret.json` file.

---

### **2️⃣ Configure Environment Variables**
Create a `.env` file in the project root:

```
# Spotify API Credentials
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

# YouTube OAuth File
YOUTUBE_OAUTH_FILE=client_secret.json
```

---

## 🚀 Running SpotiSync Locally

### **1️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Start the CLI**
```bash
python script.py
```

### **3️⃣ Available Commands**
| Command                 | Description                                      |
|-------------------------|------------------------------------------------|
| `list`                 | List all Spotify playlists                     |
| `export_youtube <id>`  | Export a Spotify playlist to YouTube Music      |
| `exit`                 | Quit the script                                 |

**Example Usage:**
```bash
list
export_youtube 3
```
*(Exports the 3rd playlist from Spotify to YouTube Music.)*

---

## 🐳 Running with Docker (GHCR)

SpotiSync is available on **GitHub Container Registry (GHCR)**:

📦 **[`ghcr.io/painteau/spotisync`](https://github.com/painteau/spotisync/pkgs/container/spotisync)**

### **1️⃣ Pull the Docker Image**
```bash
docker pull ghcr.io/painteau/spotisync:latest
```

### **2️⃣ Run the Container**
```bash
docker run --rm -it \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/client_secret.json:/app/client_secret.json \
  -p 8080:8080 \
  ghcr.io/painteau/spotisync:latest
```

### **3️⃣ Using Commands in Docker**
```bash
docker exec -it spotisync python script.py list
docker exec -it spotisync python script.py export_youtube 3
```

---

## 📂 Logs & Exported Playlists
- Export logs are saved as CSV files in the project directory.
- Format:  
  ```
  <playlist_id>.csv
  ```
- Example:
  ```
  37i9dQZF1DXcBWIGoYBM5M.csv
  ```

---

## 🔄 GitHub Actions & Automated Builds

The Docker image for **SpotiSync** is built **automatically** using **GitHub Actions**.  
Each push to the `main` branch triggers a new **Docker image build and deployment** to GHCR.

---

## 🔧 Troubleshooting
### **Authentication Issues**
If authentication fails:
1. **Verify your API keys** in `.env` and `client_secret.json`.
2. Ensure **redirect URI** in Spotify is correctly configured.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Contributing
1. Fork the repository  
2. Create a new branch (`feature-xyz`)  
3. Commit your changes  
4. Open a Pull Request  

---

## 📬 Contact
For issues or improvements, open an issue on GitHub or contact **Painteau** at **dev@gochu.fr**.

