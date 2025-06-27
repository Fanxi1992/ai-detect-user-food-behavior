import React, { useEffect, useRef } from 'react';
import { useChatStore } from '../store/chatStore';
import MessageBubble from './MessageBubble';
import StreamingMessage from './StreamingMessage';
import HealthBehaviorAnimation from './HealthBehaviorAnimation';
import NutritionCard from './NutritionCard';

const MessageList: React.FC = () => {
  const { 
    messages, 
    currentStreamingMessage, 
    isStreaming, 
    showingAnimation,
    pendingNutritionCard,
    showNutritionCardForMessage,
    setMessageAnimation
  } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage, showingAnimation]);

  // 处理动画完成，显示营养卡片
  const handleAnimationComplete = (messageId?: string) => {
    if (messageId) {
      // 消息级动画完成
      showNutritionCardForMessage(messageId);
    } else if (pendingNutritionCard) {
      // 全局动画完成（后备逻辑）
      showNutritionCardForMessage(pendingNutritionCard);
    }
  };

  // 处理营养卡片操作
  const handleNutritionCardEdit = () => {
    console.log('编辑营养记录');
    // TODO: 实现编辑功能
  };

  const handleNutritionCardDelete = () => {
    console.log('删除营养记录');
    // TODO: 实现删除功能
  };

  return (
    <div className="message-list">
      {messages.length === 0 && !isStreaming && !showingAnimation && (
        <div className="welcome-message">
          <h2>欢迎使用 AI 健康聊天助手</h2>
          <p>告诉我您的健康行为，我会帮您记录和分析！</p>
        </div>
      )}
      
      {messages.map((message) => (
        <div key={message.id}>
          <MessageBubble message={message} />
          {/* 如果该消息需要显示动画 */}
          {message.showAnimation && (
            <HealthBehaviorAnimation onComplete={() => handleAnimationComplete(message.id)} />
          )}
          {/* 如果消息有健康行为数据且需要显示营养卡片 */}
          {message.healthBehavior?.type === 'relevant' && 
           message.showNutritionCard && 
           message.healthBehavior.nutrition_data && (
            <NutritionCard 
              nutritionData={message.healthBehavior.nutrition_data}
              onEdit={handleNutritionCardEdit}
              onDelete={handleNutritionCardDelete}
            />
          )}
        </div>
      ))}
      
      {/* 保留全局动画作为后备（可以后续删除） */}
      {showingAnimation && !messages.some(msg => msg.showAnimation) && (
        <HealthBehaviorAnimation onComplete={handleAnimationComplete} />
      )}
      
      {/* 显示流式消息 */}
      {isStreaming && (
        <StreamingMessage content={currentStreamingMessage} />
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;