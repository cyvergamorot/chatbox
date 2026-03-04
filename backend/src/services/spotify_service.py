"""
Spotify Service - Handles Spotify API integration for music data
"""

import os
from typing import List, Dict, Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()


class SpotifyService:
    """
    Service for interacting with Spotify Web API
    """
    
    def __init__(self):
        """Initialize Spotify client with credentials"""
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not self.client_id or not self.client_secret:
            print("Warning: Spotify credentials not configured")
            self.client = None
            return
            
        # Set up authentication
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = spotipy.Spotify(auth_manager=auth_manager)
    
    def search_tracks(
        self, 
        query: str, 
        limit: int = 5,
        mood_genre: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for tracks on Spotify
        
        Args:
            query: Search query (genre, mood, or track name)
            limit: Number of results to return
            mood_genre: Optional mood-based genre to refine search
            
        Returns:
            List of track information dictionaries
        """
        if not self.client:
            return self._get_mock_tracks()
        
        try:
            # Build search query
            search_query = f"{query}"
            if mood_genre:
                search_query = f"genre:{mood_genre} {query}"
            
            results = self.client.search(
                q=search_query,
                type="track",
                limit=limit
            )
            
            tracks = []
            for item in results.get("tracks", {}).get("items", []):
                tracks.append(self._format_track(item))
            
            return tracks
            
        except Exception as e:
            print(f"Error searching Spotify: {e}")
            return self._get_mock_tracks()
    
    def search_playlists(
        self, 
        query: str, 
        limit: int = 3,
        mood: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for playlists on Spotify
        
        Args:
            query: Search query (mood or genre)
            limit: Number of results to return
            mood: Optional mood to refine search
            
        Returns:
            List of playlist information dictionaries
        """
        if not self.client:
            return []
        
        try:
            # Build search query
            search_query = f"{query} playlist"
            if mood:
                search_query = f"{mood} playlist"
            
            results = self.client.search(
                q=search_query,
                type="playlist",
                limit=limit
            )
            
            playlists = []
            for item in results.get("playlists", {}).get("items", []):
                if item:  # Skip None items
                    playlists.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "description": item.get("description", ""),
                        "external_urls": item.get("external_urls", {}),
                        "images": item.get("images", []),
                        "type": "playlist"
                    })
            
            return playlists
            
        except Exception as e:
            print(f"Error searching playlists: {e}")
            return []
    
    def get_recommendations(
        self, 
        mood: str, 
        limit: int = 5,
        genres: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get track recommendations based on mood
        
        Args:
            mood: The detected mood
            limit: Number of recommendations
            genres: Optional list of genres to use
            
        Returns:
            List of recommended tracks
        """
        if not self.client:
            return self._get_mock_tracks()
        
        try:
            # Map mood to Spotify seed genres
            if genres is None:
                genres = self._get_genres_for_mood(mood)
            
            # Get recommendations
            results = self.client.recommendations(
                seed_genres=genres[:5],  # Max 5 seed genres
                limit=limit
            )
            
            tracks = []
            for item in results.get("tracks", []):
                tracks.append(self._format_track(item))
            
            return tracks
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self._get_mock_tracks()
    
    def _format_track(self, track: Dict) -> Dict[str, Any]:
        """
        Format Spotify track data into our response format
        """
        return {
            "id": track.get("id"),
            "name": track.get("name"),
            "artist": ", ".join([artist["name"] for artist in track.get("artists", [])]),
            "album": track.get("album", {}).get("name"),
            "album_art": track.get("album", {}).get("images", [{}])[0].get("url"),
            "preview_url": track.get("preview_url"),
            "spotify_url": track.get("external_urls", {}).get("spotify"),
            "duration_ms": track.get("duration_ms")
        }
    
    def _get_genres_for_mood(self, mood: str) -> List[str]:
        """
        Map mood to Spotify genre seeds
        """
        mood_genre_map = {
            "happy": ["pop", "dance", "happy", "hip-hop"],
            "sad": ["sad", "indie", "bluegrass", "piano"],
            "angry": ["metal", "rock", "punk", "hardcore"],
            "calm": ["ambient", "classical", "jazz", "new-age"],
            "excited": ["dance", "edm", "pop", "party"],
            "frustrated": ["rock", "metal", "electronic", "industrial"],
            "romantic": ["r-n-b", "soul", "romance", "love-songs"],
            "nostalgic": ["pop", "rock", "soul", "disco"],
            "focused": ["classical", "instrumental", "electronic", "study"],
            "energetic": ["work-out", "edm", "hip-hop", "pop"],
            "relaxed": ["ambient", "classical", "jazz", "sleep"],
            "melancholic": ["classical", "piano", "sad", "indie"],
            "motivated": ["rock", "hip-hop", "pop", "electronic"],
            "tired": ["ambient", "classical", "soft", "new-age"]
        }
        
        return mood_genre_map.get(mood.lower(), ["pop"])
    
    def _get_mock_tracks(self) -> List[Dict[str, Any]]:
        """
        Return mock track data when Spotify is not configured
        """
        return [
            {
                "id": "mock1",
                "name": "Track Preview 1",
                "artist": "Artist Name",
                "album": "Album Name",
                "album_art": "https://via.placeholder.com/300",
                "preview_url": None,
                "spotify_url": "https://spotify.com",
                "duration_ms": 180000
            }
        ]
