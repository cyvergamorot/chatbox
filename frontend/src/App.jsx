import React, { useState, useRef, useEffect } from 'react'
import MessageBubble from './components/MessageBubble'
import PlaylistCard from './components/PlaylistCard'
import MoodPresets from './components/MoodPresets'
import MoodHistory from './components/MoodHistory'
import InputArea from './components/InputArea'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || ''  // Use proxy in dev, or direct URL in production

// Mood emojis for quick reference
const MOOD_EMOJI = {
  happy: '😊', sad: '😢', energetic: '⚡', calm: '😌',
  romantic: '💕', focused: '🎯', nostalgic: '🎭', angry: '😠'
}

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "Hi there! 🎵 I'm your music mood companion. Tell me how you're feeling today, and I'll recommend some playlists that match your mood! 😊",
      tracks: [],
      playlists: [],
      mood: 'neutral'
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [moodHistory, setMoodHistory] = useState([])
  const messagesEndRef = useRef(null)

  // Load mood history from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('moodHistory')
    if (saved) {
      try {
        setMoodHistory(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load mood history:', e)
      }
    }
  }, [])

  // Save mood history to localStorage
  const saveMoodHistory = (newHistory) => {
    setMoodHistory(newHistory)
    localStorage.setItem('moodHistory', JSON.stringify(newHistory))
  }

  // Clear all mood history
  const clearMoodHistory = () => {
    setMoodHistory([])
    localStorage.removeItem('moodHistory')
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (content) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content,
      tracks: [],
      playlists: [],
      mood: null
    }
    setMessages(prev => [...prev, userMessage])
    
    // Set loading state
    setIsLoading(true)
    
    // Add loading indicator
    const loadingId = Date.now() + 1
    setMessages(prev => [...prev, {
      id: loadingId,
      role: 'assistant',
      content: '🎵',  // Simple loading indicator
      tracks: [],
      playlists: [],
      isLoading: true
    }])

    try {
      // Build conversation history
      const conversationHistory = messages
        .filter(m => !m.isLoading)
        .map(m => ({
          role: m.role,
          content: m.content
        }))

      // Send to backend
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: content,
          conversation_history: conversationHistory
        })
      })

      if (!response.ok) {
        const errorText = await response.text()
        console.error('Response not OK:', response.status, errorText)
        throw new Error(`Server returned ${response.status}: ${errorText}`)
      }

      const data = await response.json()

      // Save mood to history if detected
      const detectedMood = data.mood_detected
      if (detectedMood && detectedMood !== 'neutral') {
        const newHistory = [
          { mood: detectedMood, timestamp: Date.now(), message: content },
          ...moodHistory
        ].slice(0, 50) // Keep only last 50
        saveMoodHistory(newHistory)
      }

      // Remove loading message and add actual response
      // Show conversational text from AI
      setMessages(prev => [
        ...prev.filter(m => m.id !== loadingId),
        {
          id: Date.now(),
          role: 'assistant',
          content: data.response || '',  // AI's conversational response
          mood: data.mood_detected,
          tracks: [],
          playlists: data.recommended_playlists || [],
          shouldRecommend: data.should_recommend
        }
      ])
    } catch (error) {
      console.error('Error:', error)
      console.error('Error message:', error.message)
      console.error('Error name:', error.name)
      // Better error message
      let errorMsg = "Sorry, I encountered an error. Please try again!"
      // Check for various network errors
      if (
        error.message.includes('Failed to fetch') ||
        error.message.includes('NetworkError') ||
        error.message.includes('network error') ||
        error.name === 'TypeError' ||
        error.message.includes('Network request failed')
      ) {
        errorMsg = "Can't connect to the server. Make sure the backend is running!"
      }
      setMessages(prev => [
        ...prev.filter(m => m.id !== loadingId),
        {
          id: Date.now(),
          role: 'assistant',
          content: errorMsg,
          tracks: [],
          playlists: [],
          mood: null
        }
      ])
    } finally {
      setIsLoading(false)
    }
  }

  // Handle mood preset selection
  const handleMoodSelect = async (mood) => {
    const moodMessage = `I'm feeling ${mood.label.toLowerCase()}`
    await sendMessage(moodMessage)
  }

  // Handle history item selection
  const handleHistorySelect = async (historyItem) => {
    const moodLabel = historyItem.mood.charAt(0).toUpperCase() + historyItem.mood.slice(1)
    const moodMessage = `I'm feeling ${moodLabel.toLowerCase()}`
    await sendMessage(moodMessage)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🎵</span>
            <h1>Music Mood Recommender</h1>
          </div>
          <p className="subtitle">AI-powered music suggestions based on your feelings</p>
        </div>
      </header>

      <main className="chat-container">
        <div className="messages-wrapper">
          {messages.map((message) => (
            <div key={message.id} className="message-wrapper">
              <MessageBubble 
                message={message} 
                isLoading={message.isLoading}
              />
              {message.playlists && message.playlists.length > 0 && (
                <div className="tracks-section">
                  <h3>📋 Playlists for you</h3>
                  <div className="tracks-grid">
                    {message.playlists.map((playlist, index) => (
                      <PlaylistCard key={playlist.id || index} playlist={playlist} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="bottom-section">
          <MoodHistory history={moodHistory} onSelectHistory={handleHistorySelect} onClear={clearMoodHistory} />
          <MoodPresets onSelectMood={handleMoodSelect} />
          <InputArea 
            onSend={sendMessage} 
            disabled={isLoading}
          />
        </div>
      </main>
    </div>
  )
}

export default App
