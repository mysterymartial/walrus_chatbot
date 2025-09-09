// SUI Chatbot API Client
import { ChatRequest, ChatResponse } from '../types/api';

/**
 * Function to query the SUI Chatbot API
 * @param query The question to ask about SUI blockchain
 * @param apiKey Optional API key for authentication
 * @returns Promise with the chat response
 */
async function askSuiChatbot(query: string, apiKey?: string): Promise<ChatResponse> {
  const request: ChatRequest = { 
    query,
    api_key: apiKey
  };
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail?.message || 'Unknown error');
    }
    
    return await response.json() as ChatResponse;
  } catch (error) {
    console.error('Error querying SUI Chatbot:', error);
    throw error;
  }
}

// Example usage
async function example() {
  try {
    const result = await askSuiChatbot('How do I create a Move module on Sui?', 'your_api_key');
    console.log('Response:', result.response);
    console.log('Processing time:', result.processing_time, 'seconds');
  } catch (error) {
    console.error('Failed to get response:', error);
  }
}

// Export the function for use in other files
export { askSuiChatbot, example };