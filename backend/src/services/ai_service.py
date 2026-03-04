"""
AI Service - Handles conversation and mood analysis using OpenAI API
"""

import os
import json
import re
from typing import Dict, List, Any
import httpx
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """
    Service for handling AI-powered conversations and mood detection
    Uses OpenAI API for natural language responses
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        
        self.system_prompt = """You are a friendly and empathetic Music Mood Recommender Bot. 
Your job is to:
1. Have natural conversations with users about any topic
2. But gently guide the conversation towards music and feelings
3. If user asks something unrelated to music, acknowledge their message warmly, then naturally transition to asking about their mood

IMPORTANT: Do NOT say "I can't help with that" or refuse to engage. Always be friendly and conversational!

When the conversation naturally leads to music or feelings, analyze their mood and include a JSON at the end:
{"mood": "detected_mood", "should_recommend": true/false}

If user is sharing feelings or wants music, set should_recommend to true. If just chatting casually, set to false.

Do NOT list song names or artist names in your response - the system will provide Spotify playlists separately.

Be warm, friendly, and always keep the conversation natural!"""
    
    async def get_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Get AI response with mood analysis
        
        Args:
            user_message: The user's input message
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary with response text, detected mood, and recommendation flag
        """
        # Build messages for API call
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        if not self.openai_api_key:
            # Fallback to simple response if no API key
            return self._fallback_response(user_message)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code != 200:
                    return self._fallback_response(user_message)
                
                data = response.json()
                response_text = data['choices'][0]['message']['content']
                
                response_text = self._strip_json_from_response(response_text)
                mood, should_recommend = self._parse_mood_from_response(response_text)
                
                return {
                    "response": response_text,
                    "mood": mood,
                    "should_recommend": should_recommend
                }
                
        except Exception as e:
            print(f"[AI Service Error]: {type(e).__name__}: {e}")
            return self._fallback_response(user_message)
    
    def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Simple fallback when no AI is available"""
        message_lower = user_message.lower()
        
        # Simple mood detection
        moods = {
            "happy": ["happy", "joy", "great", "wonderful", "good"],
            "sad": ["sad", "down", "depressed", "unhappy", "blue"],
            "angry": ["angry", "mad", "furious", "annoyed"],
            "calm": ["calm", "relaxed", "peaceful"],
            "energetic": ["energetic", "pumped", "hyper"],
            "romantic": ["love", "crush", "romantic"],
        }
        
        detected_mood = "neutral"
        for mood, keywords in moods.items():
            if any(kw in message_lower for kw in keywords):
                detected_mood = mood
                break
        
        responses = {
            "happy": "That sounds wonderful! I'm so happy for you! What kind of music makes you feel even happier?",
            "sad": "I'm sorry you're feeling down. Music can really help lift spirits. Would you like some song recommendations?",
            "angry": "I understand you're frustrated. Sometimes music can help channel those feelings. Want some music to help?",
            "calm": "That sounds peaceful. Would you like some relaxing music to match your mood?",
            "energetic": "You sound full of energy! Let me find some upbeat tracks for you!",
            "romantic": "That sounds lovely! Love songs would be perfect for this mood. Want some recommendations?",
            "neutral": "I'd love to hear more about how you're feeling! Would you like some music recommendations?"
        }
        
        return {
            "response": responses.get(detected_mood, responses["neutral"]),
            "mood": detected_mood,
            "should_recommend": True
        }
    
    def _strip_json_from_response(self, response_text: str) -> str:
        """
        Remove JSON from the AI response so it doesn't show in the chat
        """
        # Find JSON block and remove it
        start_idx = response_text.find('```json')
        if start_idx == -1:
            start_idx = response_text.find('{')
        
        if start_idx != -1:
            # Find the end of JSON (closing brace)
            end_idx = response_text.rfind('}')
            if end_idx != -1 and end_idx > start_idx:
                # Remove the JSON part
                response_text = response_text[:start_idx].strip()
                # Add a newline if there's text after
                if response_text and not response_text.endswith('.'):
                    response_text += '.'
        
        # Also remove "Here's a JSON object" text
        response_text = response_text.replace("Here's a JSON object for future reference:", "")
        response_text = response_text.replace("Here's a JSON object:", "")
        response_text = response_text.replace("JSON object:", "")
        
        # Also handle inline JSON
        response_text = re.sub(r'\{[^{}]*"mood"[^{}]*\}', '', response_text)
        response_text = re.sub(r'\s+', ' ', response_text).strip()
        
        return response_text
    
    def _parse_mood_from_response(self, response_text: str) -> tuple[str, bool]:
        """
        Parse mood and recommendation flag from AI response
        
        Looks for JSON in the response or uses keywords to determine mood
        """
        # Try to find JSON in the response
        try:
            # Look for JSON object in braces
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx+1]
                data = json.loads(json_str)
                return data.get("mood", "neutral"), data.get("should_recommend", True)
        except:
            pass
        
        # Fallback: keyword-based mood detection
        response_lower = response_text.lower()
        
        mood_keywords = {
            "happy": ["happy", "joy", "excited", "great", "wonderful"],
            "sad": ["sad", "down", "depressed", "unhappy", "blue"],
            "angry": ["angry", "mad", "frustrated", "annoyed"],
            "calm": ["calm", "relaxed", "peaceful", "serene"],
            "energetic": ["energetic", "pumped", "hyper", "wired"],
            "romantic": ["romantic", "love", "crush", "affection"],
            "nostalgic": ["nostalgic", "remember", "old days", "throwback"],
            "focused": ["focused", "concentrate", "work", "productive"]
        }
        
        for mood, keywords in mood_keywords.items():
            if any(kw in response_lower for kw in keywords):
                return mood, True
        
        return "neutral", False
