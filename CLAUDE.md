# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack AI-powered chatbot H5 application with two main components:

- **Frontend**: Located in `frontend/` - React 18.2 + TypeScript + Vite application
- **Backend**: Located in `backend/` - Planned Python FastAPI service (currently empty)

The project is designed to create a large language model-driven chatbot web application.

## Architecture

### Frontend Structure
- Built with Vite + React + TypeScript
- Uses modern React 18.2 with StrictMode
- Entry point: `src/main.tsx` renders `App.tsx` component
- Currently contains the default Vite React template

### Backend Structure
- Planned FastAPI Python backend
- Directory exists but no implementation yet
- Intended to serve as the AI/LLM integration layer

## Common Commands

### Frontend Development
All frontend commands should be run from the `frontend/` directory:

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Build Process
- TypeScript compilation followed by Vite build: `tsc -b && vite build`
- ESLint configured for code quality

## Development Workflow

1. Frontend development uses Vite's hot module replacement (HMR)
2. The project uses TypeScript with strict configuration
3. ESLint is configured for code quality enforcement
4. Backend will need to be initialized with FastAPI when development begins

## Project Context

This is a chatbot application repository focused on AI/LLM integration. The frontend will handle the chat interface while the backend will manage AI model interactions and API endpoints.