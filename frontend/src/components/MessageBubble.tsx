import React from 'react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Message } from '../store/chatStore';
import Avatar from './Avatar';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`message-bubble ${message.isUser ? 'user-message' : 'ai-message'}`}
    >
      <div className="message-wrapper">
        {/* AI消息的头像在左侧 */}
        {!message.isUser && (
          <Avatar type="ai" size="medium" />
        )}
        
        <div className="message-content-wrapper">
          <div className="message-content">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
          <div className="message-time">
            {message.timestamp.toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </div>
        </div>
        
        {/* 用户消息的头像在右侧 */}
        {message.isUser && (
          <Avatar type="user" size="medium" />
        )}
      </div>
    </motion.div>
  );
};

export default MessageBubble;