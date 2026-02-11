# Travel Planner API

A FastAPI project for managing travel projects and places, using SQLite and Art Institute API validation.

## Features
- Create travel projects with up to 10 places
- Validate places via Art Institute API
- Mark projects as completed
- Mark places as visited

## Requirements
- Docker (recommended)
- Python 3.11+ (if running locally)

## Quick Start (Docker)

1. **Build the Docker image:**
   ```bash
   docker build -t travel-planner-api .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 travel-planner-api
   ```

3. **Access the API docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables
- No required environment variables for basic usage.
- Database is stored as `test.db` in the project directory.

## Example Requests

https://web.postman.co/workspace/My-Workspace~9292a1a2-1e84-443f-8b6c-58947d2b1809/collection/39461831-b1556848-0a6b-4efd-8932-862904bd0778?action=share&source=copy-link&creator=39461831