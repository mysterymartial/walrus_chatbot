# SUI Chatbot API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A powerful API for answering questions about the SUI blockchain and Move smart contracts, leveraging AI to provide accurate and helpful responses.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
  - [Endpoints](#endpoints)
  - [Request/Response Examples](#requestresponse-examples)
- [Client Examples](#client-examples)
  - [TypeScript](#typescript)
  - [JavaScript](#javascript)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Setup](#local-setup)
  - [Environment Variables](#environment-variables)
- [Deployment](#deployment)
  - [Docker](#docker)
  - [Production Considerations](#production-considerations)
- [Development](#development)
  - [Testing](#testing)
  - [Adding New Features](#adding-new-features)
- [License](#license)

## Overview

The SUI Chatbot API provides a specialized interface for answering questions about the SUI blockchain ecosystem and Move smart contracts. It combines advanced search capabilities with AI-powered response generation to deliver accurate and contextually relevant answers.

## Features

- **AI-Powered Responses**: Utilizes OpenAI's models to generate accurate and helpful answers
- **Specialized Knowledge**: Focused on SUI blockchain, Move smart contracts, and Walrus
- **Tiered Search System**: Local SUI information database with Tavily search and DuckDuckGo fallback; Walrus queries prioritize `walruslabs.xyz` and Walrus GitHub
- **Input Validation**: Ensures queries meet length and content requirements
- **Error Handling**: Robust error management with appropriate status codes and messages
- **Docker Support**: Easy deployment with containerization
- **Configurable**: Extensive environment variable support for customization
- **Auto-Documentation**: FastAPI's built-in Swagger/OpenAPI documentation
- **Health Monitoring**: Health check endpoint for monitoring system status

### Local SUI Information Database

The API includes a built-in knowledge base about SUI blockchain fundamentals, ensuring reliable responses even when external search services are unavailable. This local database covers:

- SUI blockchain overview and key characteristics
- SUI token economics and utility
- SUI architecture and consensus mechanism
- Move programming language features
- Object-centric data model
- Transaction types and processing
- Smart contract development

The system automatically checks this local database first before querying external sources, providing faster and more reliable responses for common questions about SUI.

### Walrus Support

The chatbot now supports Walrus (on Sui) alongside Sui/Move:

- **Walrus-first search**: Walrus queries prioritize authoritative sources (`walruslabs.xyz`, Walrus GitHub) before general Sui/Move docs.
- **Price lookup**: When users ask about price/worth/market cap, the bot fetches current price via CoinGecko public API.
- **Scoped answers**: The assistant only answers Sui/Move/Walrus topics. Out-of-scope questions receive a polite message.
- **Performance**: Narrow site filters, short timeouts, and capped results for fast responses.

No additional configuration is required for Walrus price (CoinGecko public endpoints). Tavily remains optional but recommended for higher-quality results.

## Project Structure

```
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py         # API endpoints
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── dependencies.py     # Dependency injection
│   ├── data/
│   │   └── sui_info.py        # Local SUI blockchain information database
│   ├── models/
│   │   └── chat.py            # Data models
│   ├── services/
│   │   ├── ai_service.py      # AI response generation
│   │   ├── search_service.py  # Search functionality
│   │   └── validation_service.py # Input validation
│   ├── test/
│   │   ├── test_chat_api.py   # API endpoint tests
│   │   ├── test_integration.py # Integration tests
│   │   └── test_service.py    # Service unit tests
│   └── utils/
│       ├── exceptions.py      # Custom exceptions
│       └── logger.py          # Logging setup
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Pipfile                    # Pipenv dependencies
├── Pipfile.lock              # Pipenv lock file
├── pytest.ini                # Pytest configuration
└── README.md                  # Project documentation
```

## API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check endpoint |
| `/api/v1/chat` | POST | Main chat endpoint for asking questions |
| `/api/v1/info` | GET | API information and usage guidelines |
| `/` | GET | Root endpoint with basic info |

### Request/Response Examples

#### Chat Endpoint

**Request:**

```http
POST /api/v1/chat HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "query": "What is SUI blockchain?",
  "api_key": "your_api_key"
}
```

**Response:**

```json
{
  "success": true,
  "response": "SUI is a Layer 1 blockchain and smart contract platform implemented in Rust. It is designed to enable creators and developers to build experiences that cater to the next billion users in Web3. Key characteristics of SUI include high throughput and low latency, horizontal scalability, an object-centric data model, the Move programming language for smart contracts, and a proof-of-stake consensus mechanism called Narwhal and Bullshark. SUI is also the name of the native token used for gas fees, staking, and governance.",
  "query": "What is SUI blockchain?",
  "context_found": true,
  "processing_time": 5.67
}
```

#### Info Endpoint

**Request:**

```http
GET /api/v1/info HTTP/1.1
Host: localhost:8000
```

**Response:**

```json
{
  "name": "Sui Chatbot API",
  "version": "1.0.0",
  "description": "Ask questions about Sui blockchain and Move smart contracts",
  "usage": {
    "endpoint": "/chat",
    "method": "POST",
    "max_query_length": 1000,
    "supported_topics": [
      "Sui blockchain",
      "Move smart contracts",
      "Sui objects",
      "Move modules",
      "Sui transactions",
      "Move programming language"
    ]
  },
  "example_request": {
    "query": "How do I create a Move module on Sui?"
  }
}
```

### Swagger Documentation

The API includes automatic Swagger/OpenAPI documentation when running in debug mode (when `DEBUG=True` in your environment variables). Access it at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

These interactive documentation pages allow you to explore and test the API directly from your browser. The documentation is automatically generated from the FastAPI route definitions, including:

- Endpoint descriptions from docstrings
- Request/response models with validation rules
- Example requests and responses
- Authentication requirements

In production mode (`DEBUG=False`), these documentation endpoints are disabled for security reasons, as configured in `main.py`:

```python
# Import required modules
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings

# Define lifespan in main.py, not in dependencies.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API for asking questions about Sui blockchain and Move smart contracts",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan
)
```

**Note:** To enable the Swagger documentation, make sure `DEBUG=True` is set in your `.env` file. We've verified that the Swagger UI is accessible at `http://localhost:8000/docs` when debug mode is enabled.

## Client Examples

### TypeScript

```typescript
// Using fetch API with TypeScript
// Import types from the types directory
import { ChatRequest, ChatResponse } from '../types/api';

// Note: This project includes a tsconfig.json file with the following configuration:
// {
//   "compilerOptions": {
//     "target": "es6",
//     "module": "commonjs",
//     "esModuleInterop": true,
//     "strict": true,
//     "outDir": "./dist",
//     "rootDir": "./src",
//     "declaration": true,
//     "sourceMap": true
//   },
//   "include": [
//     "./src/**/*",
//     "./types/**/*"
//   ]
// }
//
// To avoid "Corresponding file is not included in tsconfig.json" error,
// make sure your TypeScript files are in the src/ or types/ directories

// This code is available in src/client.ts
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

// Note: Types are defined in types/api.d.ts
```

### JavaScript

```javascript
// Using Axios with JavaScript
const axios = require('axios');

async function askSuiChatbot(query) {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/chat', {
      query: query,
      api_key: 'your_api_key'
    });
    
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error response:', error.response.data);
      throw new Error(error.response.data.detail?.message || 'API error');
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
      throw new Error('No response from server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request error:', error.message);
      throw error;
    }
  }
}

// Example usage
async function example() {
  try {
    const result = await askSuiChatbot('What are the key features of SUI blockchain?');
    console.log('Response:', result.response);
    console.log('Processing time:', result.processing_time, 'seconds');
  } catch (error) {
    console.error('Failed to get response:', error);
  }
}

// Run the example
example();
```

## Installation

### Prerequisites

- Python 3.11+ (as used in Dockerfile)
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerized deployment)

### Dependencies

The project requires the following main dependencies:

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server for FastAPI
- OpenAI: Client for OpenAI API
- Requests: HTTP library for API calls
- Python-dotenv: Environment variable management
- Pydantic: Data validation and settings management

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/suiChatbot.git
cd suiChatbot
```

2. Install dependencies:

```bash
# Using pip
pip install -r requirements.txt

# Or using pipenv (if you prefer)
pipenv install
```

3. Set up environment variables (see [Environment Variables](#environment-variables))

4. Run the application:

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# API Configuration
APP_NAME=Sui Chatbot API
VERSION=1.0.0
DEBUG=True  # Set to False in production
HOST=0.0.0.0
PORT=8000

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
MAX_INPUT_LENGTH=1000
AI_MODEL=gpt-4o-mini  # Or another OpenAI model
AI_MAX_TOKENS=500
AI_TEMPERATURE=0.2

# Logging
LOG_LEVEL=INFO
```

These environment variables are passed to the Docker container in the `docker-compose.yml` file.

## Deployment

### Docker

The project includes Docker configuration for easy deployment:

1. Build and start the container:

```bash
docker-compose up -d --build
```

2. Check the container status:

```bash
docker-compose ps
```

3. View logs:

```bash
docker-compose logs -f
```

4. Stop the container:

```bash
docker-compose down
```

### Production Considerations

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure proper CORS settings in `main.py` (currently set to allow all origins with `allow_origins=["*"]`)
3. Set up a reverse proxy (Nginx, Traefik, etc.) with HTTPS
4. Implement rate limiting
5. Consider using a process manager like Gunicorn

Example Gunicorn command:

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Security Considerations

1. **API Keys**: Store API keys securely in environment variables or a secrets manager
2. **CORS Configuration**: Restrict allowed origins in production
3. **Input Validation**: The API already implements validation for query length
4. **Error Handling**: Avoid exposing sensitive information in error messages
5. **Rate Limiting**: Implement to prevent abuse
6. **Logging**: Be careful not to log sensitive information
7. **Dependencies**: Keep dependencies updated to avoid security vulnerabilities

## Development

### Testing

The project includes several test files in the `app/test/` directory:

- `test_chat_api.py`: Tests for the API endpoints
- `test_integration.py`: Integration tests
- `test_service.py`: Unit tests for services

Run tests using pytest:

```bash
python -m pytest
```

Or run specific test files:

```bash
python -m pytest app/tests/test_chat_api.py -v
```

### Adding New Features

1. **Add new endpoints**: Extend the router in `app/api/routes/chat.py` or create new route files
2. **Enhance search capabilities**: Modify `app/services/search_service.py`
3. **Improve AI responses**: Update the system prompt in `app/services/ai_service.py`
4. **Add new data models**: Extend `app/models/chat.py`

### Troubleshooting

#### Common Issues

1. **API Key Issues**
   - Error: "Authentication error with OpenAI API"
   - Solution: Check that your OpenAI API key is valid and properly set in the `.env` file

2. **Search Service Failures**
   - Error: "Search service failed to retrieve results"
   - Solution: Verify Tavily API key or check if DuckDuckGo fallback is working

3. **Server Won't Start**
   - Error: "Address already in use"
   - Solution: Another process is using port 8000. Either stop that process or change the port in the `.env` file

4. **Documentation Not Available**
   - Issue: Swagger UI (/docs) returns 404
   - Solution: Ensure `DEBUG=True` is set in your `.env` file

5. **Docker Issues**
   - Error: "Error starting userland proxy"
   - Solution: Another container might be using the same port. Stop it or change the port mapping in `docker-compose.yml`

### Performance Optimization

Based on our testing, the API has the following performance characteristics:

- **Simple queries**: ~5-6 seconds response time
- **Complex queries**: ~7-8 seconds response time
- **Resource usage**: Lightweight (approximately 88MB working set, 72MB private memory)

To optimize performance:

1. **Caching**: Implement a caching layer for frequent queries
2. **Model Selection**: Balance between accuracy and speed with AI model selection
3. **Concurrent Requests**: The API can handle multiple concurrent requests
4. **Search Optimization**: The tiered search system balances speed and accuracy

## License

[MIT License](LICENSE)