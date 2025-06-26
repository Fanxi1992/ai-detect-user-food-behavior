const API_BASE_URL = 'http://localhost:8000';

export interface ChatRequest {
  message: string;
  session_id: string;
}

export interface StreamChunk {
  content: string;
  done: boolean;
}

export class ChatService {
  static async sendStreamMessage(
    message: string,
    sessionId: string,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: string) => void
  ): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6); // Remove 'data: ' prefix
              if (jsonStr.trim() === '') continue;
              
              const data: StreamChunk = JSON.parse(jsonStr);
              
              if (data.done) {
                onComplete();
                return;
              } else if (data.content) {
                onChunk(data.content);
              }
            } catch (parseError) {
              console.warn('Failed to parse chunk:', line, parseError);
            }
          }
        }
      }
    } catch (error) {
      console.error('Stream error:', error);
      onError(error instanceof Error ? error.message : 'Unknown error occurred');
    }
  }

  static async getChatHistory(sessionId: string): Promise<any[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/history/${sessionId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch chat history:', error);
      return [];
    }
  }

  static async clearChatHistory(sessionId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/history/${sessionId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Failed to clear chat history:', error);
      throw error;
    }
  }
}