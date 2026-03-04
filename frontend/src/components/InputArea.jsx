import React, { useState, useRef } from 'react'

function InputArea({ onSend, disabled }) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message.trim())
      setMessage('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleChange = (e) => {
    setMessage(e.target.value)
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px'
    }
  }

  return (
    <div className="input-container">
      <form onSubmit={handleSubmit} className="input-wrapper">
        <textarea
          ref={textareaRef}
          className="input-field"
          placeholder="Tell me how you're feeling..."
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={disabled || !message.trim()}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
          </svg>
        </button>
      </form>
    </div>
  )
}

export default InputArea
