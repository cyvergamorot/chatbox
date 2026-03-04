"""
Recommendation Service - Rule engine for music recommendations
"""

from typing import List, Dict, Any, Optional


class RecommendationService:
    """
    Rule-based recommendation engine that decides when and what music to recommend
    """
    
    # Mood to music mapping
    MOOD_GENRE_MAP = {
        "happy": {
            "genres": ["happy pop", "feel good", "upbeat", "dance pop"],
            "energy": "high",
            "description": "Upbeat and joyful tracks",
            "search_terms": ["happy vibes", "feel good playlist", "upbeat pop"]
        },
        "sad": {
            "genres": ["sad songs", "heartbreak", "melancholy", "emotional"],
            "energy": "low",
            "description": "Emotional and reflective songs",
            "search_terms": ["sad playlist", "heartbreak songs", "melancholy"]
        },
        "angry": {
            "genres": ["rock", "metal", "punk", "hardcore"],
            "energy": "high",
            "description": "Powerful and intense tracks",
            "search_terms": ["angry playlist", "rock workout", "metal mood"]
        },
        "calm": {
            "genres": ["ambient", "classical", "jazz", "relaxing"],
            "energy": "low",
            "description": "Peaceful and relaxing melodies",
            "search_terms": ["calm playlist", "relaxing music", "peaceful ambient"]
        },
        "excited": {
            "genres": ["dance", "edm", "party", "pop"],
            "energy": "high",
            "description": "High-energy dance tracks",
            "search_terms": ["party playlist", "edm vibes", "dance party"]
        },
        "frustrated": {
            "genres": ["rock", "metal", "electronic", "workout"],
            "energy": "high",
            "description": "Intense and cathartic music",
            "search_terms": ["frustrated playlist", "rock workout", "release anger"]
        },
        "romantic": {
            "genres": ["r-n-b", "soul", "love songs", "romance"],
            "energy": "medium",
            "description": "Love songs and romantic ballads",
            "search_terms": ["romantic playlist", "love songs", "date night"]
        },
        "nostalgic": {
            "genres": ["90s", "80s", "classic rock", "retro"],
            "energy": "medium",
            "description": "Classic hits from the past",
            "search_terms": ["nostalgic playlist", "throwback hits", "90s classics"]
        },
        "focused": {
            "genres": ["classical", "instrumental", "study", "lo-fi"],
            "energy": "low",
            "description": "Concentration-enhancing music",
            "search_terms": ["focus playlist", "study music", "concentration"]
        },
        "energetic": {
            "genres": ["work-out", "edm", "hip-hop", "pop"],
            "energy": "high",
            "description": "Pumping workout music",
            "search_terms": ["workout playlist", "gym music", "high energy"]
        },
        "relaxed": {
            "genres": ["ambient", "chill", "sleep", "nature"],
            "energy": "low",
            "description": "Chill and unwind tracks",
            "search_terms": ["relaxed playlist", "chill vibes", "unwind music"]
        },
        "melancholic": {
            "genres": ["classical piano", "sad indie", "emotional", "rainy day"],
            "energy": "low",
            "description": "Thoughtful and introspective",
            "search_terms": ["melancholy playlist", "rainy day", "emotional piano"]
        },
        "motivated": {
            "genres": ["rock", "hip-hop", "pop", "anthem"],
            "energy": "high",
            "description": "Inspiring and empowering tracks",
            "search_terms": ["motivated playlist", "inspiration", "powerful anthems"]
        },
        "tired": {
            "genres": ["ambient", "soft piano", "sleep", "rain"],
            "energy": "low",
            "description": "Soothing and restful music",
            "search_terms": ["sleep playlist", "soft piano", "relaxing sleep"]
        },
        "neutral": {
            "genres": ["pop", "rock", "indie"],
            "energy": "medium",
            "description": "Great tracks for any mood",
            "search_terms": ["popular playlist", "top hits", "trending"]
        }
    }
    
    # Keywords to detect mood directly from user message
    MOOD_KEYWORDS = {
        "happy": ["happy", "joy", "glad", "excited", "wonderful", "great", "good", "cheerful", "delighted", "i'm happy", "feeling happy", "feel happy", "so happy"],
        "sad": ["sad", "unhappy", "depressed", "down", "blue", "melancholy", "heartbroken", "upset", "crying", "tears", "i'm sad", "feeling sad", "feel sad", "so sad", "lonely"],
        "angry": ["angry", "mad", "furious", "annoyed", "frustrated", "irritated", "hate", "rage", "i'm angry", "feeling angry", "feel angry", "so angry", "pissed"],
        "calm": ["calm", "peaceful", "relaxed", "serene", "tranquil", "content", "i'm calm", "feeling calm", "so calm"],
        "excited": ["excited", "thrilled", "pumped", "eager", "enthusiastic", "i'm excited", "so excited", "can't wait"],
        "frustrated": ["frustrated", "annoyed", "irritated", "fed up", "i'm frustrated", "so frustrated"],
        "romantic": ["romantic", "in love", "love", "crush", "affection", "i'm in love", "feeling love", "romance"],
        "nostalgic": ["nostalgic", "remember", "throwback", "old days", "miss those", "memories", "retro"],
        "focused": ["focused", "concentrate", "work", "productive", "studying", "i need to focus", "study"],
        "energetic": ["energetic", "hyper", "full of energy", "pumped", "wired", "i'm energetic", "so energetic"],
        "relaxed": ["relaxed", "chill", "chilling", "unwind", "i'm relaxed", "just chilling"],
        "melancholic": ["melancholic", "somber", "gloomy", "i'm melancholic"],
        "motivated": ["motivated", "inspired", "driven", "i'm motivated", "feeling motivated", "ready to work"],
        "tired": ["tired", "exhausted", "sleepy", "drowsy", "fatigued", "i'm tired", "so tired", "need sleep"]
    }
    
    # Keywords that indicate user wants music
    MUSIC_KEYWORDS = [
        "music", "song", "track", "playlist", "listen", "play",
        "recommend", "suggest", "hear", "tune", "jam", "melody",
        "artist", "band", "album", "genre"
    ]
    
    # Keywords that indicate user doesn't want music
    NO_MUSIC_KEYWORDS = [
        "no music", "don't want", "don't need", "not now", 
        "just chat", "talk only", "skip", "maybe later"
    ]
    
    def __init__(self, spotify_service):
        """Initialize with Spotify service"""
        self.spotify_service = spotify_service
    
    def detect_mood_from_message(self, message: str) -> str:
        """
        Detect mood directly from user message using keywords.
        This is more accurate than AI for explicit mood statements.
        
        Args:
            message: The user's message
            
        Returns:
            Detected mood string
        """
        message_lower = message.lower()
        
        # Check for mood keywords (longer phrases first for better matching)
        for mood, keywords in self.MOOD_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return mood
        
        return "neutral"
    
    def should_recommend(self, mood: str, message: str) -> bool:
        """
        Determine if music should be recommended based on mood and message
        
        Args:
            mood: Detected mood from AI
            message: User's message
            
        Returns:
            True if music should be recommended
        """
        message_lower = message.lower()
        
        # Check if user explicitly doesn't want music
        for keyword in self.NO_MUSIC_KEYWORDS:
            if keyword in message_lower:
                return False
        
        # Check if user explicitly wants music
        for keyword in self.MUSIC_KEYWORDS:
            if keyword in message_lower:
                return True
        
        # If mood is strong (not neutral), recommend music
        if mood != "neutral":
            return True
        
        return False
    
    def get_recommendations(
        self, 
        mood: str, 
        message: str = "",
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get music recommendations based on mood
        
        Args:
            mood: Detected mood
            message: User's message (for context)
            limit: Number of tracks to recommend
            
        Returns:
            List of recommended tracks
        """
        # Get genres for the mood
        mood_info = self.MOOD_GENRE_MAP.get(mood.lower(), self.MOOD_GENRE_MAP["neutral"])
        genres = mood_info["genres"]
        
        # Try Spotify recommendations first
        tracks = self.spotify_service.get_recommendations(
            mood=mood,
            limit=limit,
            genres=genres
        )
        
        # If no tracks from Spotify, search for tracks
        if not tracks or all(t.get("id") == "mock1" for t in tracks):
            search_terms = genres[:2]
            for term in search_terms:
                tracks = self.spotify_service.search_tracks(
                    query=term,
                    limit=limit,
                    mood_genre=mood
                )
                if tracks and tracks[0].get("id") != "mock1":
                    break
        
        return tracks
    
    def get_playlists(
        self, 
        mood: str, 
        limit: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Get playlist recommendations based on mood
        
        Args:
            mood: Detected mood
            limit: Number of playlists to return
            
        Returns:
            List of recommended playlists
        """
        mood_info = self.MOOD_GENRE_MAP.get(mood.lower(), self.MOOD_GENRE_MAP["neutral"])
        search_terms = mood_info.get("search_terms", mood_info["genres"])
        
        # Search for playlists
        playlists = []
        for term in search_terms[:3]:
            results = self.spotify_service.search_playlists(
                query=term,
                limit=limit,
                mood=mood
            )
            if results:
                playlists.extend(results)
        
        # Remove duplicates
        seen = set()
        unique_playlists = []
        for p in playlists:
            if p.get("id") not in seen:
                seen.add(p.get("id"))
                unique_playlists.append(p)
        
        return unique_playlists[:limit]
    
    def get_mood_description(self, mood: str) -> str:
        """
        Get a description for the detected mood
        """
        mood_info = self.MOOD_GENRE_MAP.get(mood.lower(), self.MOOD_GENRE_MAP["neutral"])
        return mood_info["description"]
    
    def get_mood_emoji(self, mood: str) -> str:
        """
        Get an emoji representation of the mood
        """
        mood_emoji_map = {
            "happy": "😊",
            "sad": "😢",
            "angry": "😠",
            "calm": "😌",
            "excited": "🤩",
            "frustrated": "😤",
            "romantic": "💕",
            "nostalgic": "🎭",
            "focused": "🎯",
            "energetic": "⚡",
            "relaxed": "😴",
            "melancholic": "🌧️",
            "motivated": "💪",
            "tired": "😴",
            "neutral": "😐"
        }
        return mood_emoji_map.get(mood.lower(), "🎵")
