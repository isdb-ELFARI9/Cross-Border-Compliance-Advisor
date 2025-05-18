# Cross-Border Compliance Advisor

A sophisticated system for managing and analyzing Shariah compliance in cross-border financial operations. This project provides tools for regulatory compliance analysis, Shariah compliance checking, and automated regulation management.

## Features

- **Compliance Analysis**: Automated analysis of financial regulations for Shariah compliance
- **Regulatory Management**: Tools for drafting, updating, and revising regulations
- **QA System**: Intelligent query processing for regulatory compliance questions
- **Cross-Border Support**: Specialized handling of international regulatory requirements

## Project Structure

```
.
├── api/                    # API implementation
├── data/                   # Data storage
├── data_cross_border/      # Cross-border specific data
├── docs/                   # Documentation
├── src/                    # Source code
├── static/                 # Static assets
└── tests/                  # Test files
```

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ComplianceAdvisor
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### API Server

You can run the API server using one of the provided scripts:

```bash
# Simple API
./run_api_simple.sh

# Structured API
./run_api_structured.sh

# Compatibility API
./run_compat_api.sh
```

Or directly with Uvicorn:

```bash
uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

### Using the API Client

```python
from api_client import ComplianceAdvisorClient

# Initialize client
client = ComplianceAdvisorClient(base_url="http://localhost:8000")

# Example: Process a compliance query
result = client.process_qa_query("What are the compliance risks with current liquidity policies?")
```

## Key Dependencies

- FastAPI: Web framework for building APIs
- LangChain: Framework for developing applications powered by language models
- Google Generative AI: Integration with Google's AI services
- Pinecone: Vector database for semantic search
- Pydantic: Data validation and settings management
- SQLAlchemy: SQL toolkit and ORM

## Development

### Running Tests

```bash
pytest
```

### Environment Setup

For development environment setup:

```bash
./setup_compat_env.sh
```

## Documentation

- API Documentation: See `api_README.md` and `api_README_structured.md`
- Additional documentation is available in the `docs/` directory

