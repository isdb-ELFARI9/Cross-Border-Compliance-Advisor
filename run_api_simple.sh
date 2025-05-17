#!/bin/bash

# Set up environment variable for development
export DEBUG="True"

# Clean up any existing installation
pip uninstall -y pydantic pydantic-core fastapi uvicorn

# Install specific versions of packages directly
echo "Installing compatible packages..."
pip install "fastapi==0.78.0" "uvicorn==0.18.2" "pydantic==1.9.1" python-dotenv==1.0.0 jinja2==3.1.2 requests==2.31.0

# Run the FastAPI application directly
echo "Starting API server..."
cd "$(dirname "$0")"
PYTHONPATH=. uvicorn api.core.app:app --host 0.0.0.0 --port 8000 --reload
