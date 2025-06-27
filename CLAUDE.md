# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack AI-powered health chatbot H5 application that integrates real AI models through OpenRouter API. The application features intelligent health behavior recognition and nutrition tracking capabilities:

- **Frontend**: React 18.2 + TypeScript + Vite + Zustand for state management + TailwindCSS
- **Backend**: Python FastAPI + SQLite + OpenRouter integration for real AI model calls + Health behavior detection service
- **Core Features**: 
  - Real-time streaming chat with health behavior analysis
  - Intelligent nutrition tracking and food recognition
  - Persistent chat history with health data
  - Session management with dual AI avatar system
  - Real-time health behavior animations and nutrition cards

## Architecture

### Frontend Structure (`frontend/`)
- **Framework**: Vite + React 18.2 + TypeScript + TailwindCSS
- **State Management**: Zustand (`src/store/chatStore.ts`) with health behavior tracking
- **Components**:
  - `ChatContainer.tsx`: Main chat interface with history loading and health behavior integration
  - `MessageList.tsx`: Displays chat messages with nutrition cards and animations
  - `ChatInput.tsx`: User input interface
  - `MessageBubble.tsx`: Individual message display with avatar system
  - `StreamingMessage.tsx`: Real-time streaming message display
  - `Avatar.tsx`: Multi-type avatar system (user/ai/health) with different designs
  - `HealthBehaviorAnimation.tsx`: Real-time thinking animation during health analysis
  - `NutritionCard.tsx`: Interactive nutrition information display cards
- **Services**: `chatService.ts` - API communication with backend for chat and health detection
- **Styles**: Modular CSS files for components (`styles/` directory)
- **Entry Point**: `src/main.tsx` → `App.tsx` → `ChatContainer.tsx`

### Backend Structure (`backend/`)
- **Framework**: FastAPI with async/await support
- **Database**: SQLite with aiosqlite for async operations
- **AI Integration**: OpenRouter service for real LLM API calls + Health behavior detection
- **Core Files**:
  - `main.py`: FastAPI application with streaming endpoints and health behavior integration
  - `database.py`: SQLite operations for message persistence with health behavior data
  - `openrouter_service.py`: OpenRouter API integration for chat completions
  - `health_behavior_service.py`: AI-powered health behavior detection and nutrition analysis
  - `health_behavior_schema.py`: Structured schema definitions for health behavior detection
  - `models.py`: Pydantic models for request/response including health behavior data
  - `config.py`: Configuration management for API keys and models

### Data Flow Architecture

1. **Message Rendering Logic**:
   - Frontend uses Zustand store to cache messages with health behavior data in `messages: Message[]`
   - On page load: Fetches history from backend database via `/api/chat/history/{session_id}`
   - During chat: New messages added directly to frontend state with health behavior tracking
   - Display: Messages rendered from frontend state with nutrition cards and animations

2. **Health Behavior Detection Flow**:
   ```
   User Input → Save to DB → Health Behavior Detection (LLM) → 
   Extract Nutrition Data → Update Message → Display Animation → 
   Show Nutrition Card → Continue Chat Flow
   ```

3. **Dual-Phase Streaming Response Flow**:
   - **Phase 1**: Health behavior detection
     - User sends message via POST `/api/chat/stream`
     - Backend saves user message immediately
     - Calls health behavior detection service with structured output
     - Returns health behavior result (`type: 'health_behavior'`)
     - Frontend shows thinking animation and nutrition card if relevant
   - **Phase 2**: Normal chat completion
     - Retrieves last 10 messages from database
     - Calls OpenRouter API with conversation context
     - Streams AI response chunks in real-time to frontend (`type: 'chat'`)
     - Saves complete AI response to database when done

4. **Health Behavior Data Structure**:
   ```typescript
   interface HealthBehaviorData {
     type: 'relevant' | 'unrelevant';
     nutrition_data?: {
       food_name: string;
       calories: number;
       protein: number;
       carbs: number;
       fat: number;
       meal_type: string; // 早餐/午餐/晚餐/上午加餐/下午加餐/夜宵
     } | null;
   }
   ```

## API Endpoints

### Chat Endpoints
- `POST /api/chat/stream` - Streaming chat with AI (main endpoint)
- `POST /api/chat` - Non-streaming chat completion
- `GET /api/chat/history/{session_id}` - Retrieve chat history
- `DELETE /api/chat/history/{session_id}` - Clear chat history

### System Endpoints  
- `GET /api/health` - Health check
- `GET /api/config` - Check OpenRouter configuration status

## Environment Configuration

### Backend Environment Variables
Create a `.env` file in the `backend/` directory:
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here
DEFAULT_MODEL=openai/gpt-4o-mini
HEALTH_DETECTION_MODEL=openai/gpt-4o-mini  # Model for health behavior detection (must support structured output)
```

## Common Commands

### Frontend Development
Run from `frontend/` directory:
```bash
npm install          # Install dependencies
npm run dev          # Start development server (http://localhost:5173)
npm run build        # Build for production (TypeScript + Vite)
npm run lint         # Lint code with ESLint
npm run preview      # Preview production build
```

### Backend Development
Run from `backend/` directory:
```bash
pip install -r requirements.txt    # Install Python dependencies
python main.py                     # Start FastAPI server (http://localhost:8000)
```

### Full Stack Development
1. Terminal 1: `cd backend && python main.py`
2. Terminal 2: `cd frontend && npm run dev`
3. Access application at `http://localhost:5173`

## Database Schema

### SQLite Tables
- **messages**: Stores all chat messages with health behavior data
  - `id`: TEXT PRIMARY KEY (UUID)
  - `session_id`: TEXT (chat session identifier)
  - `content`: TEXT (message content)
  - `is_user`: BOOLEAN (true for user messages, false for AI)
  - `timestamp`: DATETIME
  - `health_behavior_data`: TEXT (JSON string containing health behavior detection results)

## Key Technical Features

1. **Real-time Streaming**: Server-Sent Events for live AI response streaming with dual-phase processing
2. **Health Behavior Detection**: AI-powered recognition of nutrition and health-related user inputs
3. **Structured AI Output**: Using JSON Schema for consistent health behavior analysis results
4. **Session Management**: UUID-based session tracking for conversation continuity
5. **State Management**: Zustand for efficient frontend state handling with health behavior tracking
6. **Interactive Nutrition Cards**: Dynamic nutrition information display with meal type categorization
7. **Thinking Animations**: Real-time visual feedback during health behavior analysis
8. **Dual Avatar System**: Different avatars for user, AI, and health-related interactions
9. **Error Handling**: Comprehensive error handling for API failures with fallback mechanisms
10. **Responsive Design**: Mobile-friendly chat interface with health behavior components
11. **Database Persistence**: SQLite for reliable message storage with health behavior data

## Health Behavior Detection System

### AI-Powered Nutrition Analysis
The application uses a dedicated AI service (`health_behavior_service.py`) that:
- Analyzes user input for health and nutrition-related content
- Extracts structured nutrition data using JSON Schema validation
- Provides meal type categorization based on time context
- Returns nutrition information including calories, protein, carbs, and fat

### Meal Type Classification
Supports Chinese meal categories:
- 早餐 (Breakfast): 06:00-09:00
- 上午加餐 (Morning Snack): 09:00-11:00  
- 午餐 (Lunch): 11:00-14:00
- 下午加餐 (Afternoon Snack): 14:00-17:00
- 晚餐 (Dinner): 17:00-21:00
- 夜宵 (Late Night Snack): 21:00-06:00

### Frontend Health Behavior Integration
- `HealthBehaviorAnimation.tsx`: Shows thinking animation during analysis
- `NutritionCard.tsx`: Displays structured nutrition information
- `Avatar.tsx`: Uses health-specific avatar for nutrition-related messages
- Store integration: Health behavior data persisted in Zustand store