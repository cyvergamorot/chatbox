# Music Mood Recommender Bot

An AI-powered chatbot that understands your feelings and recommends music based on your mood. Built with React, FastAPI, Ollama (local AI), and Spotify API.

## Features

- **AI Conversation**: Uses Ollama with Mistral model for local, free AI-powered conversations
- **Smart Recommendations**: Rule-based engine maps moods to appropriate music genres
- **Spotify Integration**: Get real track recommendations from Spotify
- **Modern Chat UI**: Clean, responsive interface with playlist cards
- **Mood Presets**: Quick-select buttons for common moods
- **Mood History**: Tracks your conversation history locally

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                   │
│                    http://localhost:5173                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Chat UI    │  │ Mood Presets  │  │   Mood History         │ │
│  └─────────────┘  └──────────────┘  └────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP POST /api/chat
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI + Python)                 │
│                      http://localhost:8000                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Main Application                        │  │
│  │  ┌─────────────┐  ┌─────────────────┐  ┌─────────────┐  │  │
│  │  │ AI Service  │  │ Recommendation  │  │  Spotify    │  │  │
│  │  │ (Ollama)    │  │    Service      │  │  Service    │  │  │
│  │  └─────────────┘  └─────────────────┘  └─────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│   OLLAMA (Local AI)     │     │      SPOTIFY API            │
│   mistral model         │     │   Track & Playlist Search   │
│   http://localhost:11434 │     │   Recommendations           │
└─────────────────────────┘     └─────────────────────────────┘
```

## Prerequisites

- **Node.js 18+** - For running the frontend
- **Python 3.9+** - For running the backend
- **Spotify Developer Account** - For music recommendations
- **Ollama** - For local AI (free, runs locally)

## Installation & Setup

### Step 1: Install Ollama (Required)

Ollama provides local AI inference - no API keys needed, runs completely offline.

**Windows:**
1. Download from https://ollama.com/download/windows
2. Run the installer
3. Open a terminal and verify: `ollama --version`

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Start Ollama service:**
```bash
ollama serve
```
Keep this terminal open (or run as a background service).

**Pull the Mistral model:**
```bash
ollama pull mistral
```

### Step 2: Clone and Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend:**
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Configure Spotify API (Optional but Recommended)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy your **Client ID** and **Client Secret**
4. Create a `.env` file in the `backend/` directory:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
PORT=8000
HOST=0.0.0.0
```

> **Note:** If you skip this, the app will use mock data for tracks.

## How to Run the System

### Option 1: Run Both Services Separately

**Terminal 1 - Start Ollama (if not running as service):**
```bash
ollama serve
```

**Terminal 2 - Start Backend:**
```bash
cd backend
# Activate virtual environment if needed
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux

python -m src.main
# Backend will start at http://localhost:8000
```

**Terminal 3 - Start Frontend:**
```bash
cd frontend
npm run dev
# Frontend will start at http://localhost:5173
```

### Option 2: Quick Start Script (Windows)

Create a file `start.bat` in the project root:
```batch
@echo off
echo Starting Music Mood Recommender...
echo.
echo Starting Backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate && python -m src.main"
echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo System starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
pause
```

### Option 3: Using Uvicorn Directly

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## How the System Works

### Data Flow

1. **User Input**: User types a message describing their mood or feelings in the chat

2. **Frontend Processing**: React app sends the message to the backend API (`/api/chat`)

3. **AI Analysis (Ollama)**: 
   - The backend sends the message to the local Ollama service
   - Ollama uses the Mistral model to understand the user's mood
   - Returns a conversational response and detected mood

4. **Keyword Detection (Fallback)**:
   - The `RecommendationService` also uses keyword matching
   - This provides more accurate mood detection for explicit statements
   - e.g., "I'm happy" → detects "happy" mood

5. **Music Recommendation**:
   - Based on the detected mood, the system maps to appropriate genres
   - Spotify API is called to get real track and playlist recommendations
   - If Spotify is not configured, mock data is returned

6. **Response to User**:
   - Frontend displays playlist cards with Spotify links
   - Mood history is saved to localStorage

### Key Components

| Component | File | Description |
|-----------|------|-------------|
| FastAPI App | `backend/src/main.py` | Main API server, handles /api/chat endpoint |
| AI Service | `backend/src/services/ai_service.py` | Connects to Ollama for mood analysis |
| Recommendation Service | `backend/src/services/recommendation_service.py` | Rule-based engine for mood detection and music mapping |
| Spotify Service | `backend/src/services/spotify_service.py` | Handles Spotify API calls |
| React App | `frontend/src/App.jsx` | Main frontend application |
| Chat Components | `frontend/src/components/` | UI components (MessageBubble, PlaylistCard, etc.) |

## Mood Mapping

The system maps detected moods to appropriate music genres:

| Mood | Genres | Description |
|------|--------|-------------|
| Happy | pop, dance, happy | Upbeat and joyful tracks |
| Sad | sad, indie, piano | Emotional and reflective songs |
| Angry | rock, metal, punk | Powerful and intense tracks |
| Calm | ambient, classical, jazz | Peaceful and relaxing melodies |
| Excited | dance, edm, party | High-energy dance tracks |
| Romantic | r-n-b, soul, romance | Love songs and romantic ballads |
| Focused | classical, instrumental | Concentration-enhancing music |
| Energetic | work-out, edm, hip-hop | Pumping workout music |
| Relaxed | ambient, chill, sleep | Chill and unwind tracks |
| Nostalgic | 90s, 80s, classic rock | Classic hits from the past |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API health check |
| `/api/health` | GET | Health status |
| `/api/chat` | POST | Main chat endpoint |

### Chat API Request
```json
{
  "message": "I'm feeling really happy today!",
  "conversation_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ]
}
```

### Chat API Response
```json
{
  "response": "That's wonderful to hear! Music is great for amplifying good moods.",
  "mood_detected": "happy",
  "recommended_tracks": [...],
  "recommended_playlists": [...],
  "should_recommend": true
}
```

## Tech Stack

- **Frontend**: React 18, Vite, CSS3
- **Backend**: Python 3.9+, FastAPI, Uvicorn
- **AI**: Ollama (Mistral model) - Local, free inference
- **Music API**: Spotify Web API
- **Authentication**: Spotify Client Credentials Flow

## Troubleshooting

### Ollama Issues

**"connection refused" error:**
- Make sure Ollama is running: `ollama serve`
- Check Ollama is on port 11434

**Model not found:**
- Pull the model: `ollama pull mistral`

### Spotify Issues

**"No tracks found":**
- Verify your Spotify credentials in `backend/.env`
- Check Spotify Developer Dashboard for app status

### Frontend Issues

**"Cannot connect to server":**
- Ensure backend is running on port 8000
- Check the proxy configuration in `vite.config.js`

## License

MIT


To expose your locally running app to the internet, use Cloudflare Tunnel.

### Step 1: Start the Backend Tunnel

Open a new terminal and run:
```
cd c:\Users\Eli\chatbot
cloudflared.exe tunnel --url http://localhost:8000
```
Copy the URL shown (for example, https://xxxx.trycloudflare.com)

### Step 2: Start the Frontend Tunnel

Open another terminal and run:
```
cd c:\Users\Eli\chatbot
cloudflared.exe tunnel --url http://localhost:5173
```

### Step 3: Update Frontend Configuration

After getting your tunnel URLs:

1. Edit `frontend/src/App.jsx` - change the API_URL to your backend tunnel URL
2. Edit `frontend/vite.config.js` - add your frontend tunnel URL to allowedHosts array

### Important Notes

- Cloudflare tunnel URLs change every time you restart cloudflared
- Each time you get a new URL, you need to update both files above
- For local testing without tunnels, use http://localhost:5173


