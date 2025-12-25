FastAPI AI Agent API

This project provides a backend API built with FastAPI to interface with Large Language Models (LLMs) via the OpenRouter gateway. The architecture is designed to provide a stable and secure foundation for AI-driven applications, following modern software engineering principles.

Technical Features
- Modular architecture with clear separation between business logic and data validation.
- Resilience mechanisms including retry logic and timeout management for external API requests.
- Secure credential management using environment variables.
- Automated API documentation and testing interface via Swagger UI.

Requirements
- Python 3.9 or higher.
- An active OpenRouter API access key.

Installation and Setup
1. Install the necessary dependencies:
   pip install -r requirements.txt

2. Configuration:
   Create a .env file in the root directory and add your credentials:
   OPENROUTER_API_KEY=your_actual_api_key_here

3. Execution:
   Run the development server using:
   uvicorn app.main:app --reload

Security Best Practices
Sensitive configuration files and virtual environments are excluded from version control via .gitignore to ensure credential security and repository cleanliness.