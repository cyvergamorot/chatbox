import React from 'react'
import './PlaylistCard.css'

function PlaylistCard({ playlist }) {
  const spotifyUrl = playlist.external_urls?.spotify || '#'
  const imageUrl = playlist.images?.[0]?.url || 'https://via.placeholder.com/300'
  
  return (
    <a 
      href={spotifyUrl} 
      target="_blank" 
      rel="noopener noreferrer" 
      className="playlist-card"
    >
      <div className="playlist-image">
        <img src={imageUrl} alt={playlist.name} />
        <div className="playlist-play-overlay">
          <span className="play-icon">▶</span>
        </div>
      </div>
      <div className="playlist-info">
        <h4 className="playlist-name">{playlist.name}</h4>
        {playlist.description && (
          <p className="playlist-description">
            {playlist.description.replace(/<[^>]*>/g, '').substring(0, 60)}...
          </p>
        )}
        <span className="playlist-open">Open in Spotify →</span>
      </div>
    </a>
  )
}

export default PlaylistCard
