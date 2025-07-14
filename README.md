# LLM Backend Playground

A modular multi-agent backend for routing natural language queries to the right tool (math, weather, LLM, etc.) using FastAPI, LangGraph, and Gemini/OpenAI APIs.

---

## 🚀 Quickstart

### Option 1: Automated Setup (Recommended)
```bash
git clone <your-repo-url>
cd llm_be_playground
make setup  # This will install all prerequisites and set up the environment
```

### Option 2: Manual Setup
1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd llm_be_playground
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```


---

## 🐳 Docker Deployment (Recommended)

### Using Docker Compose (Easiest)
```bash
# Build and run with docker-compose (uses git version tagging)
make docker-compose-up

# Build latest version (no cache)
make docker-compose-build

# View logs
make docker-compose-logs

# Stop the service
make docker-compose-down
```

### Using Docker directly
```bash
# Build the image with git version tagging
make docker-build

# Build latest version (no cache)
make docker-build-latest

# Run the container with specific git version
make docker-run

# Run the container with latest tag
make docker-run-latest

# Stop the container
make docker-stop

# Clean up (stop and remove container/image)
make docker-clean

# Show current version info
make version
```

### Manual Docker commands
```bash
# Build with git version
GIT_VERSION=$(git describe --tags --always --dirty) docker build -t llm-be-playground:${GIT_VERSION} -t llm-be-playground:latest .

# Run with environment file
docker run --env-file .env -p 8000:8000 llm-be-playground:${GIT_VERSION}

# Or run with docker-compose (uses git version automatically)
GIT_VERSION=$(git describe --tags --always --dirty) docker-compose up -d
```

---

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip
- virtual environment (created automatically)

### Setup and Run
```bash
# Install dependencies and create virtual environment
make install

# Run in development mode (with auto-reload)
make dev

# Or run in production mode
make run
```

---

## 📝 Project Structure

### Root Directory
- `app/` - Main application code
- `Dockerfile` - Container configuration for deployment
- `docker-compose.yml` - Multi-container orchestration with git versioning
- `Makefile` - Development and deployment automation with git versioning
- `setup.sh` - Automated environment setup script
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `logs/` - Application logs directory
- `.dockerignore` - Docker build exclusions

### Application Architecture (`app/`)

#### Core Components
- **`main.py`** - FastAPI application entry point with REST endpoints
- **`config.py`** - Application settings and environment configuration
- **`models.py`** - Pydantic data models and type definitions
- **`agents.py`** - LangGraph agents for intent classification and processing
- **`workflow.py`** - LangGraph workflow definition and routing logic

#### Tools Module (`app/tools/`)
- **`math_tools.py`** - Mathematical expression evaluation
- **`weather_tools.py`** - Weather data retrieval and processing
- **`llm_tools.py`** - Generic LLM-based question answering
- **`__init__.py`** - Tool module exports

### Data Flow Architecture

```
User Query → FastAPI (main.py) 
    ↓
Intent Classification (agents.py)
    ↓
LangGraph Workflow (workflow.py)
    ↓
Tool Routing → Specific Tools (tools/)
    ↓
Response Generation → User
```

### Key Design Patterns

1. **Multi-Agent System**: Uses LangGraph agents for intent classification and task routing
2. **Tool-Based Architecture**: Modular tools for different query types (math, weather, general)
3. **State Management**: QueryState model tracks query processing through the workflow
4. **Configuration Management**: Centralized settings with environment variable support

---

## 🔑 Environment Variables
See `.env.example` for all required variables:
- `GEMINI_API_KEY` (required for Gemini LLM)
- `OPENWEATHER_API_KEY` (for weather queries)
- ...and more

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **LangGraph** - Multi-agent workflow orchestration
- **Pydantic-AI** - LLM integration and agent management

### AI/ML Components
- **Google Gemini** - Primary LLM for intent classification and general queries
- **OpenWeatherMap API** - Weather data retrieval
- **Mathematical Expression Evaluation** - Safe math computation

### Development & Deployment
- **Docker** - Containerization for consistent deployment
- **Docker Compose** - Multi-service orchestration
- **Uvicorn** - ASGI server for FastAPI
- **Python 3.11+** - Modern Python with type hints support

---

## 🧪 Testing the API
After running (locally or with Docker):
- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI
- Or use curl:
  ```bash
  curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{"query": "What is 2 + 2?"}'
  ```

## 🔌 API Endpoints

### Core Endpoints
- **`GET /`** - Health check and API status
- **`GET /health`** - Detailed health status
- **`POST /query`** - Main query processing endpoint

### Query Processing Flow
1. **Intent Classification**: The system analyzes the query to determine intent (math, weather, or general)
2. **Tool Routing**: Based on intent, routes to appropriate specialized tool
3. **Response Generation**: Tool processes query and returns structured response

### Supported Query Types
- **Mathematical**: "What is 15 * 23?", "Calculate 2^10"
- **Weather**: "What's the weather in Tokyo?", "Temperature in New York"
- **General**: "What is machine learning?", "Explain quantum computing"

---

## 🛠️ Available Make Commands

### Development
- `make install` - Install Python dependencies
- `make dev` - Run in development mode with auto-reload
- `make run` - Run in production mode
- `make clean` - Clean up Python cache files

### Docker
- `make docker-build` - Build Docker image with git version tagging
- `make docker-build-latest` - Build latest version (no cache)
- `make docker-run` - Run Docker container with specific git version
- `make docker-run-latest` - Run Docker container with latest tag
- `make docker-stop` - Stop Docker container
- `make docker-clean` - Stop and remove Docker container/image
- `make version` - Show current git version and image details

### Docker Compose
- `make docker-compose-up` - Start with docker-compose (uses git versioning)
- `make docker-compose-build` - Build latest version with docker-compose
- `make docker-compose-down` - Stop docker-compose services
- `make docker-compose-logs` - View docker-compose logs

### Setup
- `make setup` - Run automated setup script

---

## 📦 Production
- Use Docker for deployment with git version tagging
- Healthcheck endpoint: `/health`
- Exposes port 8000 by default
- Docker Compose includes restart policy, health checks, and version labels
- Images are tagged with git version for precise version control

---

## 🔧 Setup Script Features

The `setup.sh` script automatically:
- Detects your operating system (Ubuntu, CentOS, Fedora, macOS)
- Installs Python 3.11+ if not present
- Installs Docker if not present
- Installs curl for health checks
- Creates Python virtual environment
- Installs all Python dependencies
- Builds Docker image
- Provides colored output and error handling

## 🏷️ Git Versioning

The project includes automatic git versioning for Docker images:

### Version Tagging
- **Automatic**: Images are tagged with git version using `git describe --tags --always --dirty`
- **Dual Tags**: Each build creates both version-specific and `latest` tags
- **Examples**: 
  - `llm-be-playground:v1.2.3` (tagged release)
  - `llm-be-playground:dev-abc123` (development commit)
  - `llm-be-playground:latest` (always points to most recent build)

### Version Information
```bash
# Show current version details
make version

# Output example:
# Git Version: v1.2.3
# Git Commit: abc123
# Image Name: llm-be-playground
# Image Tag: v1.2.3
```

### Benefits
- **Reproducibility**: Run exact versions for debugging or rollbacks
- **Tracking**: Container labels include version and commit info
- **Flexibility**: Choose between specific versions or latest
- **CI/CD Ready**: Perfect for automated deployment pipelines

---

## License
MIT 