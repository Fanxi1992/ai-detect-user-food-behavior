import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

export interface NutritionData {
  food_name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  meal_type: string;
}

export interface HealthBehaviorData {
  type: 'relevant' | 'unrelevant';
  nutrition_data?: NutritionData;
  confidence: number;
  detected_keywords?: string[];
}

export interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  healthBehavior?: HealthBehaviorData;
  showNutritionCard?: boolean;
}

interface ChatState {
  messages: Message[];
  currentStreamingMessage: string;
  isStreaming: boolean;
  inputDisabled: boolean;
  sessionId: string;
  currentHealthBehavior: HealthBehaviorData | null;
  showingAnimation: boolean;
  pendingNutritionCard: string | null; // 存储待显示营养卡片的消息ID
  
  // Actions
  addMessage: (content: string, isUser: boolean, healthBehavior?: HealthBehaviorData) => void;
  updateStreamingMessage: (chunk: string) => void;
  finishStreaming: () => void;
  startStreaming: () => void;
  setInputDisabled: (disabled: boolean) => void;
  clearChat: () => void;
  setMessages: (messages: Message[]) => void;
  setHealthBehavior: (data: HealthBehaviorData) => void;
  setShowingAnimation: (showing: boolean) => void;
  setPendingNutritionCard: (messageId: string | null) => void;
  showNutritionCardForMessage: (messageId: string) => void;
  updateMessageHealthBehavior: (messageId: string, healthBehavior: HealthBehaviorData) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  currentStreamingMessage: '',
  isStreaming: false,
  inputDisabled: false,
  sessionId: uuidv4(),
  currentHealthBehavior: null,
  showingAnimation: false,
  pendingNutritionCard: null,
  
  addMessage: (content: string, isUser: boolean, healthBehavior?: HealthBehaviorData) => {
    const newMessage: Message = {
      id: uuidv4(),
      content,
      isUser,
      timestamp: new Date(),
      healthBehavior,
      showNutritionCard: false,
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
      currentHealthBehavior: null,
      showingAnimation: false,
      pendingNutritionCard: null,
    });
  },
  
  setMessages: (messages: Message[]) => {
    set({ messages });
  },
  
  setHealthBehavior: (data: HealthBehaviorData) => {
    set({ currentHealthBehavior: data });
  },
  
  setShowingAnimation: (showing: boolean) => {
    set({ showingAnimation: showing });
  },
  
  setPendingNutritionCard: (messageId: string | null) => {
    set({ pendingNutritionCard: messageId });
  },
  
  showNutritionCardForMessage: (messageId: string) => {
    set((state) => ({
      messages: state.messages.map(msg => 
        msg.id === messageId 
          ? { ...msg, showNutritionCard: true }
          : msg
      ),
      pendingNutritionCard: null,
      showingAnimation: false, // 关闭动画状态
    }));
  },
  
  updateMessageHealthBehavior: (messageId: string, healthBehavior: HealthBehaviorData) => {
    set((state) => ({
      messages: state.messages.map(msg => 
        msg.id === messageId 
          ? { ...msg, healthBehavior }
          : msg
      ),
    }));
  },
}));