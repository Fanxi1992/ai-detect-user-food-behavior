import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../store/chatStore';
import { ChatService } from '../services/chatService';

const ChatInput: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const [isKeyboardVisible, setIsKeyboardVisible] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const { 
    inputDisabled, 
    isStreaming, 
    sessionId,
    addMessage, 
    startStreaming, 
    updateStreamingMessage, 
    finishStreaming 
  } = useChatStore();

  // 自动调整输入框高度
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
    }
  };

  // 键盘显示/隐藏检测
  useEffect(() => {
    const handleResize = () => {
      if (window.visualViewport) {
        const viewportHeight = window.visualViewport.height;
        const windowHeight = window.innerHeight;
        const threshold = windowHeight * 0.75; // 键盘占用超过25%屏幕高度时认为键盘弹起
        
        setIsKeyboardVisible(viewportHeight < threshold);
      }
    };

    const handleFocus = () => {
      // 延迟检测，等待键盘完全弹起
      setTimeout(() => {
        if (window.visualViewport) {
          const viewportHeight = window.visualViewport.height;
          const windowHeight = window.innerHeight;
          setIsKeyboardVisible(viewportHeight < windowHeight * 0.75);
        }
      }, 300);
    };

    const handleBlur = () => {
      setTimeout(() => {
        setIsKeyboardVisible(false);
      }, 300);
    };

    // 监听viewport变化
    if (window.visualViewport) {
      window.visualViewport.addEventListener('resize', handleResize);
    }

    // 监听输入框焦点事件
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.addEventListener('focus', handleFocus);
      textarea.addEventListener('blur', handleBlur);
    }

    return () => {
      if (window.visualViewport) {
        window.visualViewport.removeEventListener('resize', handleResize);
      }
      if (textarea) {
        textarea.removeEventListener('focus', handleFocus);
        textarea.removeEventListener('blur', handleBlur);
      }
    };
  }, []);

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputValue.trim() || inputDisabled) {
      return;
    }

    const message = inputValue.trim();
    setInputValue('');
    
    // 添加用户消息
    addMessage(message, true);
    
    // 开始流式响应
    startStreaming();
    
    // 发送流式请求
    await ChatService.sendStreamMessage(
      message,
      sessionId,
      (chunk: string) => {
        updateStreamingMessage(chunk);
      },
      () => {
        finishStreaming();
      },
      (error: string) => {
        console.error('Chat error:', error);
        let errorMessage = '发送消息失败，请稍后重试';
        
        if (error.includes('Failed to fetch')) {
          errorMessage = '网络连接失败，请检查后端服务是否正常运行';
        } else if (error.includes('500')) {
          errorMessage = '服务器内部错误，请稍后重试';
        } else if (error.includes('404')) {
          errorMessage = 'API接口不存在，请检查后端配置';
        }
        
        addMessage(`❌ ${errorMessage}`, false);
        finishStreaming();
      }
    );
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className={`chat-input-container ${isKeyboardVisible ? 'keyboard-visible' : ''}`}>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={isStreaming ? "AI正在回复中..." : "输入消息..."}
          disabled={inputDisabled}
          className="chat-textarea"
          rows={1}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || inputDisabled}
          className={`send-button ${inputDisabled ? 'disabled' : ''}`}
        >
          {isStreaming ? (
            <div className="loading-spinner"></div>
          ) : (
            <svg 
              width="20" 
              height="20" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor"
            >
              <path d="M22 2L11 13"></path>
              <path d="M22 2L15 22L11 13L2 9L22 2Z"></path>
            </svg>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInput;