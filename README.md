# AI PowerPoint Generator

A web application that converts a user's text prompt into a complete PowerPoint presentation using AI.

## Features

- Simple web interface to input your presentation topic
- AI-powered content generation via Deepseek API
- Automatic creation of PowerPoint presentations with python-pptx
- Clean architecture for maintainability and testability

## Requirements

- Python 3.8+
- Deepseek API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Deepseek API key:
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
   ```

## Usage

1. Start the server:
   ```
   python main.py
   ```
2. Open your browser and navigate to `http://localhost:8000`
3. Enter your prompt describing the presentation you want
4. Click "Generate Presentation"
5. Download the generated PowerPoint file

## Project Structure

The application follows clean architecture principles:

- `domain/`: Core business entities and interfaces
- `application/`: Use cases and DTOs
- `infrastructure/`: External services implementation (Deepseek API, PowerPoint generation)
- `presentation/`: API endpoints and web interface

## Deployment on Render

This application is ready to be deployed on Render using the following steps:

1. Push this code to a Git repository
2. Create a new Web Service on Render, pointing to your repository
3. Use the "Python 3" runtime
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add your environment variables (DEEPSEEK_API_KEY, DEEPSEEK_API_URL)
7. Deploy the service

## License

MIT