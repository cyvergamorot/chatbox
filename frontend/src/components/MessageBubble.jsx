import React from 'react'
import './MessageBubble.css'

const MOOD_EMOJIS = {
  happy: '😊',
  sad: '😢',
  angry: '😠',
  calm: '😌',
  excited: '🤩',
  frustrated: '😤',
  romantic: '💕',
  nostalgic: '🎭',
  focused: '🎯',
  energetic: '⚡',
  relaxed: '😴',
  melancholic: '🌧️',
  motivated: '💪',
  tired: '😴',
  neutral: '🎵'
}

function MessageBubble({ message, isLoading }) {
  const isUser = message.role === 'user'
  const moodEmoji = message.mood ? MOOD_EMOJIS[message.mood] || '🎵' : null

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="avatar">
        {isUser ? '👤' : '🎵'}
      </div>
      <div className="bubble-content">
        {isLoading ? (
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        ) : (
          <>
            <p>{message.content}</p>
            {message.mood && !isUser && (
              <span className="mood-badge">
                {moodEmoji} Feeling: {message.mood}
              </span>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
