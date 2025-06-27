# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack AI-powered chatbot H5 application that integrates real AI models through OpenRouter API. The application features:

- **Frontend**: React 18.2 + TypeScript + Vite + Zustand for state management
- **Backend**: Python FastAPI + SQLite + OpenRouter integration for real AI model calls
- **Features**: Real-time streaming chat, persistent chat history, session management

## Architecture

### Frontend Structure (`frontend/`)
- **Framework**: Vite + React 18.2 + TypeScript
- **State Management**: Zustand (`src/store/chatStore.ts`)
- **Components**:
  - `ChatContainer.tsx`: Main chat interface with history loading
  - `MessageList.tsx`: Displays chat messages
  - `ChatInput.tsx`: User input interface
  - `MessageBubble.tsx`: Individual message display
  - `StreamingMessage.tsx`: Real-time streaming message display
- **Services**: `chatService.ts` - API communication with backend
- **Entry Point**: `src/main.tsx` → `App.tsx` → `ChatContainer.tsx`

### Backend Structure (`backend/`)
- **Framework**: FastAPI with async/await support
- **Database**: SQLite with aiosqlite for async operations
- **AI Integration**: OpenRouter service for real LLM API calls
- **Core Files**:
  - `main.py`: FastAPI application with streaming endpoints
  - `database.py`: SQLite operations for message persistence
  - `openrouter_service.py`: OpenRouter API integration
  - `models.py`: Pydantic models for request/response

### Data Flow Architecture

1. **Message Rendering Logic**:
   - Frontend uses Zustand store to cache messages in `messages: Message[]`
   - On page load: Fetches history from backend database via `/api/chat/history/{session_id}`
   - During chat: New messages added directly to frontend state (no database queries)
   - Display: Messages rendered from frontend state, not real-time database queries

2. **Backend Business Logic**:
   ```
   User Input → Save to DB → Fetch History → Format for AI → 
   Call OpenRouter → Stream Response → Save AI Response → Return to Frontend
   ```

3. **Streaming Response Flow**:
   - User sends message via POST `/api/chat/stream`
   - Backend saves user message immediately
   - Retrieves last 10 messages from database
   - Calls OpenRouter API with conversation context
   - Streams AI response chunks in real-time to frontend
   - Saves complete AI response to database when done

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
```

## Common Commands

### Frontend Development
Run from `frontend/` directory:
```bash
npm install          # Install dependencies
npm run dev          # Start development server (http://localhost:5173)
npm run build        # Build for production
npm run lint         # Lint code
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
- **messages**: Stores all chat messages
  - `id`: TEXT PRIMARY KEY (UUID)
  - `session_id`: TEXT (chat session identifier)
  - `content`: TEXT (message content)
  - `is_user`: BOOLEAN (true for user messages, false for AI)
  - `timestamp`: DATETIME

## Key Technical Features

1. **Real-time Streaming**: Server-Sent Events for live AI response streaming
2. **Session Management**: UUID-based session tracking for conversation continuity
3. **State Management**: Zustand for efficient frontend state handling
4. **Error Handling**: Comprehensive error handling for API failures
5. **Responsive Design**: Mobile-friendly chat interface
6. **Database Persistence**: SQLite for reliable message storage