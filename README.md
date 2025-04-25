# Julep Research Assistant

A FastAPI-based web service that uses Julep AI to provide research assistance on various topics.

## Features

- Research topics and present findings in various formats (summary, bullet points, short report)
- RESTful API with FastAPI
- Docker support for easy deployment
- Clean, modular project structure

## Project Structure

```
julep-research-assistant/
│
├── app/                         # Application package
│   ├── api/                     # API endpoints
│   ├── core/                    # Core application components
│   └── services/                # Business logic services
│
├── tests/                       # Test suite
├── .env.example                 # Example environment variables
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── main.py                      # Application entry point
└── requirements.txt             # Project dependencies
```

## Setup and Installation

### Prerequisites

- Python 3.9+
- Julep API key

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/julep-research-assistant.git
cd julep-research-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your Julep API key.

6. Run the application:
```bash
python main.py
```

### Docker Deployment

1. Build and start the Docker container:
```bash
docker-compose up -d
```

2. Stop the container:
```bash
docker-compose down
```

## API Usage

### Research Endpoint

**POST /research**

Request body:
```json
{
  "topic": "artificial intelligence ethics",
  "format": "bullet points"
}
```

Response:
```json
{
  "topic": "artificial intelligence ethics",
  "format": "bullet points",
  "result": "• AI ethics concerns the moral implications of AI systems.\n• Key issues include privacy, bias, and accountability.\n• Many organizations have developed ethical guidelines for AI.\n• Ethical AI requires diverse perspectives.\n• Challenges include balancing innovation with safety."
}
```

## License

[MIT](LICENSE)