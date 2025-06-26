import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

export interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  currentStreamingMessage: string;
  isStreaming: boolean;
  inputDisabled: boolean;
  sessionId: string;
  
  // Actions
  addMessage: (content: string, isUser: boolean) => void;
  updateStreamingMessage: (chunk: string) => void;
  finishStreaming: () => void;
  startStreaming: () => void;
  setInputDisabled: (disabled: boolean) => void;
  clearChat: () => void;
  setMessages: (messages: Message[]) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  currentStreamingMessage: '',
  isStreaming: false,
  inputDisabled: false,
  sessionId: uuidv4(),
  
  addMessage: (content: string, isUser: boolean) => {
    const newMessage: Message = {
      id: uuidv4(),
      content,
      isUser,
      timestamp: new Date(),
    };
    
    set((state) => ({
      messages: [...state.messages, newMessage],
    }));
  },
  
  updateStreamingMessage: (chunk: string) => {
    set((state) => ({
      currentStreamingMessage: state.currentStreamingMessage + chunk,
    }));
  },
  
  finishStreaming: () => {
    const { currentStreamingMessage } = get();
    if (currentStreamingMessage.trim()) {
      get().addMessage(currentStreamingMessage, false);
    }
    
    set({
      currentStreamingMessage: '',
      isStreaming: false,
      inputDisabled: false,
    });
  },
  
  startStreaming: () => {
    set({
      isStreaming: true,
      inputDisabled: true,
      currentStreamingMessage: '',
    });
  },
  
  setInputDisabled: (disabled: boolean) => {
    set({ inputDisabled: disabled });
  },
  
  clearChat: () => {
    set({
      messages: [],
      currentStreamingMessage: '',
      isStreaming: false,
      inputDisabled: false,
    });
  },
  
  setMessages: (messages: Message[]) => {
    set({ messages });
  },
}));