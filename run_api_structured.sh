#!/bin/bash

# Set up environment variable for development
export DEBUG="True"

# Clean up pydantic first to avoid version conflicts
echo "Cleaning up pydantic installation..."
pip uninstall -y pydantic pydantic-core

# Install API requirements with specific compatible versions
echo "Installing API requirements..."
pip install fastapi==0.88.0 uvicorn==0.22.0 python-dotenv==1.0.0 jinja2==3.1.2 pydantic==1.10.8 requests==2.31.0

# Run the FastAPI application using the new structured code
echo "Starting API server..."
python -m uvicorn api.core.app:app --host 0.0.0.0 --port 8000 --reload
