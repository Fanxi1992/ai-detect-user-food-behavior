import React from 'react';
import '../styles/avatar.css';

interface AvatarProps {
  type: 'user' | 'ai' | 'health';
  size?: 'small' | 'medium' | 'large';
}

const Avatar: React.FC<AvatarProps> = ({ type, size = 'medium' }) => {
  const getAvatarContent = () => {
    switch (type) {
      case 'user':
        return '👤';
      case 'ai':
        return '🤖';
      case 'health':
        return '🏥';
      default:
        return '👤';
    }
  };

  const getAvatarColor = () => {
    switch (type) {
      case 'user':
        return '#667eea';
      case 'ai':
        return '#4299e1';
      case 'health':
        return '#48bb78';
      default:
        return '#667eea';
    }
  };

  return (
    <div 
      className={`avatar avatar-${size} avatar-${type}`}
      style={{ backgroundColor: getAvatarColor() }}
    >
      <span className="avatar-icon">
        {getAvatarContent()}
      </span>
    </div>
  );
};

export default Avatar;