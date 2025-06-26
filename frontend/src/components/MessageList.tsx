import React, { useEffect, useRef } from 'react';
import { useChatStore } from '../store/chatStore';
import MessageBubble from './MessageBubble';
import StreamingMessage from './StreamingMessage';

const MessageList: React.FC = () => {
  const { messages, currentStreamingMessage, isStreaming } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage]);

  return (
    <div className="message-list">
      {messages.length === 0 && !isStreaming && (
        <div className="welcome-message">
          <h2>欢迎使用 AI 聊天助手</h2>
          <p>有什么可以帮助您的吗？</p>
        </div>
      )}
      
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      
      {isStreaming && (
        <StreamingMessage content={currentStreamingMessage} />
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;