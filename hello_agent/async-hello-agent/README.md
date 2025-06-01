# Async Hello Agent

A simple async agent built using Google's Gemini API that demonstrates basic async functionality.

## Setup

1. Make sure you have Poetry installed
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Agent

To run the agent:

```bash
poetry run python async_hello_agent.py
```

## Features

- Async implementation using Python's asyncio
- Uses nest_asyncio for nested event loop support
- Simple greeting functionality using Google's Gemini API
- Environment variable management with python-dotenv

## Dependencies

- google-generativeai
- nest-asyncio
- python-dotenv
- Python 3.12+ 