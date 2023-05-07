#!/bin/bash

# Apply database migrations
alembic upgrade head

# Load initial data
python3 todos/scripts/initial_data.py

# Start the FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000