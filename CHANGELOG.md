# Changelog

All notable changes to SpotiSync will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive pagination support for all Spotify and YouTube API calls
- Rate limiting (100ms delay) to prevent YouTube API quota exceeded errors
- Lazy loading for YouTube authentication (only authenticates when needed)
- Playlist caching to reduce redundant API calls
- Automatic `logs/` directory creation for CSV exports
- Comprehensive error handling for all API operations
- Missing `add_video_to_playlist()` function with rate limiting
- `.gitignore` file for Python project best practices
- Formatted console table output for import results with summary statistics

### Changed
- Improved `list_playlists()` to handle 50+ playlists with pagination
- Enhanced `get_playlist_tracks()` to support playlists of any size
- Upgraded `get_youtube_playlists()` with pagination support
- Better error messages for debugging across all functions
- CSV logs now saved to `logs/` directory instead of project root
- Optimized main loop with playlist caching

### Fixed
- Missing `add_video_to_playlist()` function that caused runtime errors
- Removed dependency on `ace_tools` which was not in requirements.txt
- Playlist truncation when accessing playlists beyond the first 50 items
- Track truncation when exporting playlists with more than 100 songs
- YouTube API calls without proper error handling
- Null pointer exceptions when tracks have missing artist information
- Authentication blocking for Spotify-only operations

### Removed
- `ace_tools` dependency replaced with native console formatting

## [1.0.0] - Initial Release

### Added
- Spotify to YouTube Music playlist transfer functionality
- Browse and list Spotify playlists from CLI
- Playlist name consistency across platforms
- Conflict handling with overwrite and duplicate modes
- CSV export logs for transferred playlists
- Docker support with GHCR integration
- GitHub Actions for automated Docker builds
- Environment variable configuration support
- OAuth authentication for both Spotify and YouTube

### Security
- OAuth 2.0 authentication for Spotify API
- OAuth 2.0 authentication for YouTube API
- Environment variable support for sensitive credentials
- `.gitignore` configuration to prevent credential commits
