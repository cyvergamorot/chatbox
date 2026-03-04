import React from 'react'
import './MoodPresets.css'

const MOODS = [
  { id: 'happy', emoji: '😊', label: 'Happy' },
  { id: 'sad', emoji: '😢', label: 'Sad' },
  { id: 'energetic', emoji: '⚡', label: 'Energetic' },
  { id: 'calm', emoji: '😌', label: 'Calm' },
  { id: 'romantic', emoji: '💕', label: 'Romantic' },
  { id: 'focused', emoji: '🎯', label: 'Focused' },
  { id: 'nostalgic', emoji: '🎭', label: 'Nostalgic' },
  { id: 'angry', emoji: '😠', label: 'Angry' },
]

function MoodPresets({ onSelectMood }) {
  return (
    <div className="mood-presets">
      <div className="mood-buttons">
        {MOODS.map((mood) => (
          <button
            key={mood.id}
            className="mood-button"
            onClick={() => onSelectMood(mood)}
          >
            <span className="mood-emoji">{mood.emoji}</span>
            <span className="mood-label">{mood.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}

export default MoodPresets
