# 🎵 SpotiSync - Spotify to YouTube Music Playlist Converter

SpotiSync is a **Python-based CLI tool** that exports playlists from **Spotify** and imports them into **YouTube Music**.
This project is fully containerized on **GitHub Container Registry (GHCR)**.

---

## ⭐ Features
- 🔍 **Browse & List**: View all your **Spotify playlists** directly from the CLI with **full pagination support**.
- 🔄 **Playlist Transfer**: Export a **Spotify playlist** to **YouTube Music** seamlessly.
- 🎵 **Name Consistency**: Maintain the **same playlist name** across both platforms.
- ⚡ **Conflict Handling**:
  - **Overwrite Mode**: Delete and recreate existing playlists.
  - **Duplicate Mode**: Create a new playlist with a different name.
- 📊 **Export Logs**: Generate detailed **CSV logs** for every transferred playlist (saved in `logs/` directory).
- 🛠 **Automation**: Integrated **GitHub Actions** for automated **Docker builds** and updates.
- 🚀 **Performance Optimized**:
  - **Pagination**: Handle playlists of any size (50+ playlists, 100+ tracks).
  - **Rate Limiting**: Built-in delays to prevent API quota errors.
  - **Smart Caching**: Reduce redundant API calls with intelligent playlist caching.
  - **Lazy Loading**: YouTube authentication only when needed.
- 🛡️ **Robust Error Handling**: Comprehensive error management for all API operations.

---

## 📌 Prerequisites

### **Spotify API Keys**
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create a **new application**.
3. Obtain your **Client ID** and **Client Secret**.
4. Set a **Redirect URI**:
   ```
   http://localhost:8888/callback
   ```

### **Google OAuth for YouTube**
1. Open the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create an **OAuth 2.0 Client ID**.
3. Choose **"Desktop App"**.
4. Download the `client_secret.json` file.

---

## 🛠 Setup & Installation

### **1️⃣ Configure Environment Variables**
Create a `.env` file in the project root:

```
# Spotify API Credentials
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

# YouTube OAuth File
YOUTUBE_OAUTH_FILE=client_secret.json
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Start the CLI**
```bash
python script.py
```

### **4️⃣ Available Commands**
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

## 🔨 Running SpotiSync Locally

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/painteau/spotisync.git
cd spotisync
```

### **2️⃣ Set Up Environment Variables**
Follow the instructions in the **Setup & Installation** section.

### **3️⃣ Run the Application**
```bash
python script.py
```

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
docker run -d --rm --label com.centurylinklabs.watchtower.enable=true \  
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

## ⚙ Configuration
| Option                  | Description                                      |
|-------------------------|------------------------------------------------|
| `.env` File             | Stores API credentials                         |
| `client_secret.json`    | OAuth credentials for YouTube                  |
| `logs/*.csv`            | Exported playlist logs                         |

---

## 🔧 Troubleshooting

### **Authentication Issues**
If authentication fails:
1. **Verify your API keys** in `.env` and `client_secret.json`.
2. Ensure **redirect URI** in Spotify is correctly configured.
3. Delete `.cache` files if experiencing persistent authentication issues.

### **Large Playlist Issues**
If you have playlists with many tracks:
- The tool now automatically handles pagination for playlists of any size.
- Built-in rate limiting prevents YouTube API quota errors.

### **API Quota Errors**
If you encounter quota errors:
- The tool includes automatic rate limiting (100ms delay between operations).
- Consider spreading large transfers across multiple sessions.

---

## 📝 Recent Improvements

### Version 1.1.0 (Latest)
- ✅ Fixed missing `add_video_to_playlist()` function
- ✅ Added full pagination support for all API calls
- ✅ Implemented rate limiting to prevent quota errors
- ✅ Added lazy loading for YouTube authentication
- ✅ Improved error handling across all operations
- ✅ Optimized performance with smart caching
- ✅ CSV logs now saved to dedicated `logs/` directory
- ✅ Enhanced console output with formatted tables

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## ⚠ Security Notice
Ensure that you expose the Docker container securely and restrict access if necessary when deploying in a production environment.

---

## 💡 Contributing
1️⃣ **Fork** the repository on [GitHub](https://github.com/painteau/spotisync)  
2️⃣ **Create a new branch** (`feature-branch`)  
3️⃣ **Commit your changes**  
4️⃣ **Push to your branch and create a pull request**  

For major changes, please open an **issue** first to discuss the proposed modifications.

---

## 📬 Contact
For issues or improvements, open an issue on GitHub or contact **Painteau** at **dev@gochu.fr**.

