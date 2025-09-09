// TypeScript definitions for SUI Chatbot API client

export interface ChatRequest {
  query: string;
  api_key?: string;
}

export interface ChatResponse {
  success: boolean;
  response: string;
  query: string;
  context_found: boolean;
  processing_time: number;
}