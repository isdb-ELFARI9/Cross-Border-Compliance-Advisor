# Cross-Border Compliance Advisor API

A RESTful API for Shariah compliance analysis and regulatory management.

## Architecture

The API follows a clean, modular architecture:

```
api/
├── core/           # Core application components
│   ├── app.py      # FastAPI application setup
│   ├── config.py   # Configuration settings
│   └── logging.py  # Logging setup
├── models/         # Data models and validation
│   ├── base.py
│   ├── qa_transform.py
│   ├── regulation_drafting.py
│   └── regulation_update.py
├── routes/         # API endpoint routes
│   ├── health.py
│   ├── qa_transform.py
│   ├── regulation_drafting.py
│   └── regulation_update.py
├── services/       # Business logic and services
│   └── orchestrator_service.py
├── utils/          # Utility functions
│   └── file_utils.py
└── main.py         # Entry point
```

## Features

This API provides endpoints to:

1. **Health Check** - Check if the API and all services are available
2. **QA Transform AAOIFI** - Process regulatory queries using specialized agents
3. **Regulation Drafting** - Analyze and update regulations for Shariah compliance
4. **Regulation Update & Revision** - Analyze regulations for compliance issues

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository (if not already done):

```bash
git clone <repository-url>
cd Cross-Border-Compliance-Advisor
```

2. Install the API requirements:

```bash
pip install -r api_requirements.txt
```

### Running the API

You can run the API using the provided shell script:

```bash
./run_api_structured.sh
```

Or directly with Python:

```bash
python -m api.main
```

The API will be available at http://0.0.0.0:8000

### API Documentation

Once the API is running, you can access the auto-generated documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the API and all services.

### QA Transform AAOIFI

```
POST /api/qa-transform
```

Process a regulatory query and get a comprehensive answer.

**Request Body:**
```json
{
  "text": "What are the compliance risks with current liquidity policies?"
}
```

### Regulation Drafting

```
POST /api/regulation-drafting
```

Process regulations for Shariah compliance analysis.

**Request Body:**
```json
{
  "regulations": {
    // Regulation data (see data/regulations.json for format)
  }
}
```

### Regulation Update & Revision

```
POST /api/regulation-update
```

Analyze regulations for compliance issues.

**Request Body:**
```json
{
  "regulations": {
    // Regulation data (see data/regulations.json for format)
  }
}
```

## Using the API Client

The API comes with a Python client for easy integration:

```python
from api_client import ComplianceAdvisorClient

# Initialize client
client = ComplianceAdvisorClient("http://localhost:8000")

# Check health
health = client.health_check()

# Process a query
result = client.process_qa_query("What are the compliance risks with current liquidity policies?")

# Process regulations
with open("data/regulations.json", "r") as f:
    regulations = json.load(f)
    
drafting_result = client.process_regulation_drafting(regulations)
update_result = client.process_regulation_update(regulations)
```

## Development

### Project Structure

- **api/** - The API code
- **src/** - Core business logic and orchestrators
- **data/** - Sample data and outputs
- **static/** - Static files (HTML, CSS, JS)

### Adding New Features

To add new features to the API:

1. Create any needed models in `api/models/`
2. Add business logic in `api/services/`
3. Create route handlers in `api/routes/`
4. Register the new routes in `api/core/app.py`

### Running Tests

Tests can be run using pytest:

```bash
pytest -xvs api/tests
```

## License

[Your License Here]

## Contact

[Your Contact Information]
