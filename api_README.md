# Cross-Border Compliance Advisor API

A RESTful API for interacting with the Cross-Border Compliance Advisor system, providing Shariah compliance analysis and regulatory management functionalities.

## Features

The API provides the following endpoints:

1. **QA Transform AAOIFI**: Process regulatory queries and get comprehensive answers
2. **Regulation Drafting**: Analyze and update regulations for Shariah compliance
3. **Regulation Update & Revision**: Merge reports from compliance scanner and propagator agents

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
./run_api.sh
```

Or directly with Uvicorn:

```bash
uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at http://localhost:8000 in your web browser.
You can access the interactive API documentation at http://localhost:8000/docs.

## API Endpoints

### Health Check

```
GET /health
```

Returns the health status of the API and its services.

### QA Transform

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
    "External Regulation": [...],
    "Internal Rulebook": [...]
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
    "External Regulation": [...],
    "Internal Rulebook": [...]
  }
}
```

## Using the API Client

For convenience, a Python client is provided to interact with the API:

```python
from api_client import ComplianceAdvisorClient

# Initialize the client
client = ComplianceAdvisorClient(base_url="http://localhost:8000")

# Check API health
health = client.health_check()
print(f"Health status: {health}")

# Process a query
query_result = client.process_qa_query("What are the compliance risks with current liquidity policies?")
print(f"Final answer: {query_result.get('final_answer')}")
```

## License

[Your License Information]

## Contact

[Your Contact Information]
