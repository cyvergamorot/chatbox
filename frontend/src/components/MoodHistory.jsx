import React from 'react'
import './MoodHistory.css'

const MOOD_CONFIG = {
  happy: { emoji: '😊', label: 'Happy' },
  sad: { emoji: '😢', label: 'Sad' },
  energetic: { emoji: '⚡', label: 'Energetic' },
  calm: { emoji: '😌', label: 'Calm' },
  romantic: { emoji: '💕', label: 'Romantic' },
  focused: { emoji: '🎯', label: 'Focused' },
  nostalgic: { emoji: '🎭', label: 'Nostalgic' },
  angry: { emoji: '😠', label: 'Angry' },
  neutral: { emoji: '😐', label: 'Neutral' },
}

function MoodHistory({ history, onSelectHistory, onClear }) {
  if (!history || history.length === 0) {
    return null
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date
    
    if (diff < 60000) return 'now'
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h`
    return date.toLocaleDateString()
  }

  return (
    <div className="mood-history">
      <div className="mood-history-header">
        <span className="mood-history-title">Recent: </span>
        {onClear && (
          <button 
            className="mood-history-clear" 
            onClick={onClear}
            title="Clear history"
          >
            ✕
          </button>
        )}
      </div>
      <div className="mood-history-list">
        {history.slice(0, 6).map((item, index) => {
          const config = MOOD_CONFIG[item.mood] || MOOD_CONFIG.neutral
          return (
            <button
              key={index}
              className="mood-history-item"
              onClick={() => onSelectHistory(item)}
              title={`${config.label} - ${formatTime(item.timestamp)}`}
            >
              <span className="history-emoji">{config.emoji}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default MoodHistory
