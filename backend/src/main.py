"""
Music Mood Recommender Bot - Backend Server
FastAPI application for AI-powered music recommendations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

from src.services.ai_service import AIService
from src.services.spotify_service import SpotifyService
from src.services.recommendation_service import RecommendationService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Music Mood Recommender Bot",
    description="AI-powered chatbot that recommends music based on your mood",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
spotify_service = SpotifyService()
recommendation_service = RecommendationService(spotify_service)


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    mood_detected: str
    recommended_tracks: List[Dict[str, Any]]
    recommended_playlists: List[Dict[str, Any]]
    should_recommend: bool


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Music Mood Recommender Bot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user message and returns AI response with music recommendations
    """
    try:
        # Get AI response (includes mood analysis and conversational response)
        ai_result = await ai_service.get_response(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        # Extract mood from AI response
        ai_mood = ai_result.get("mood", "neutral")
        conversational_response = ai_result.get("response", "")
        
        # Use keyword-based mood detection (more accurate than AI)
        # This directly detects mood from user message
        mood_detected = recommendation_service.detect_mood_from_message(request.message)
        
        # If keyword detection returns neutral, fall back to AI detection
        if mood_detected == "neutral":
            mood_detected = ai_mood
        
        # Determine if we should recommend music
        should_recommend = recommendation_service.should_recommend(
            mood=mood_detected,
            message=request.message
        )
        
        # Get music recommendations if appropriate
        recommended_tracks = []
        recommended_playlists = []
        if should_recommend:
            recommended_tracks = recommendation_service.get_recommendations(
                mood=mood_detected,
                message=request.message
            )
            # Also get playlist recommendations
            recommended_playlists = recommendation_service.get_playlists(
                mood=mood_detected
            )
        
        return ChatResponse(
            response=conversational_response,
            mood_detected=mood_detected,
            recommended_tracks=recommended_tracks,
            recommended_playlists=recommended_playlists,
            should_recommend=should_recommend
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
