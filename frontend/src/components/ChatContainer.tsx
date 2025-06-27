import React, { useEffect, useState } from 'react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import { useChatStore } from '../store/chatStore';
import { ChatService } from '../services/chatService';

const ChatContainer: React.FC = () => {
  const { clearChat, setMessages, sessionId } = useChatStore();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 加载最近的聊天历史（全局）
  useEffect(() => {
    const loadHistory = async () => {
      try {
        setIsLoading(true);
        const history = await ChatService.getRecentChatHistory(20);
        const messages = history.map((msg: any) => ({
          id: msg.id || Math.random().toString(),
          content: msg.content,
          isUser: msg.is_user,
          timestamp: new Date(msg.timestamp),
          // 恢复健康行为数据
          healthBehavior: msg.health_behavior_data || undefined,
          // 如果有健康行为数据且类型为relevant，则显示营养卡片
          showNutritionCard: msg.health_behavior_data?.type === 'relevant' && !!msg.health_behavior_data?.nutrition_data,
          showAnimation: false, // 历史记录不显示动画
        }));
        setMessages(messages);
      } catch (err) {
        console.error('Failed to load chat history:', err);
        setError('加载聊天历史失败');
      } finally {
        setIsLoading(false);
      }
    };

    loadHistory();
  }, [setMessages]); // 移除 sessionId 依赖，因为我们现在加载全局历史

  const handleClearChat = async () => {
    if (window.confirm('确定要清空所有聊天记录吗？此操作将删除数据库中的所有历史记录。')) {
      try {
        await ChatService.clearAllChatHistory();
        clearChat();
        setError(null);
      } catch (err) {
        console.error('Failed to clear all chat history:', err);
        setError('清空聊天历史失败');
      }
    }
  };

  if (isLoading) {
    return (
      <div className="chat-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>加载聊天历史中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      {/* 聊天头部 */}
      <div className="chat-header">
        <h1>AI 聊天助手</h1>
        <button 
          onClick={handleClearChat}
          className="clear-button"
          title="清空聊天"
        >
          <svg 
            width="18" 
            height="18" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor"
          >
            <path d="M3 6H5H21"></path>
            <path d="M8 6V4C8 3.44772 8.44772 3 9 3H15C15.5523 3 16 3.44772 16 4V6M19 6V20C19 20.5523 18.5523 21 18 21H6C5.44772 21 5 20.5523 5 20V6H19Z"></path>
          </svg>
        </button>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)} className="error-close">
            ×
          </button>
        </div>
      )}

      {/* 消息区域 */}
      <div className="chat-messages">
        <MessageList />
      </div>

      {/* 输入区域 */}
      <div className="chat-input-area">
        <ChatInput />
      </div>
    </div>
  );
};

export default ChatContainer;