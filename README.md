# FastAPI Demo

A complete FastAPI backend application with CRUD operations, health checks, and containerization support.

## Features

- ✅ `/health` endpoint for health checks
- ✅ `/users` CRUD endpoints (Create, Read, Update, Delete) with in-memory storage
- ✅ Pydantic models for data validation
- ✅ Comprehensive pytest test suite
- ✅ Docker and docker-compose support
- ✅ Makefile for easy development workflow

## Project Structure

```
fastapi-demo/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application with endpoints
│   └── models.py        # Pydantic models
├── tests/
│   ├── __init__.py
│   ├── test_health.py   # Tests for /health endpoint
│   └── test_users.py    # Tests for /users endpoints
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11+
- Docker (optional, for containerized deployment)

## Setup and Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/VishalPrasanna11/fastapi-demo.git
   cd fastapi-demo
   ```

2. **Install dependencies**
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   make run
   # or
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with docker-compose**
   ```bash
   make docker-up
   # or
   docker-compose up
   ```

2. **Build the Docker image only**
   ```bash
   make docker-build
   # or
   docker-compose build
   ```

3. **Stop the services**
   ```bash
   make docker-down
   # or
   docker-compose down
   ```

## API Endpoints

### Health Check

- **GET** `/health` - Check if the API is running
  ```bash
  curl http://localhost:8000/health
  ```
  Response: `{"status": "healthy"}`

### Users

- **GET** `/users` - Get all users
  ```bash
  curl http://localhost:8000/users
  ```

- **GET** `/users/{user_id}` - Get a specific user by ID
  ```bash
  curl http://localhost:8000/users/1
  ```

- **POST** `/users` - Create a new user
  ```bash
  curl -X POST http://localhost:8000/users \
    -H "Content-Type: application/json" \
    -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
  ```

- **PUT** `/users/{user_id}` - Update an existing user
  ```bash
  curl -X PUT http://localhost:8000/users/1 \
    -H "Content-Type: application/json" \
    -d '{"name": "John Smith", "email": "johnsmith@example.com", "age": 31}'
  ```

- **DELETE** `/users/{user_id}` - Delete a user
  ```bash
  curl -X DELETE http://localhost:8000/users/1
  ```

## Testing

Run the test suite:

```bash
make test
# or
pytest -v
```

The test suite includes:
- Health endpoint tests
- User CRUD operation tests
- Validation tests
- Error handling tests

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install Python dependencies |
| `make run` | Run the FastAPI application locally |
| `make test` | Run pytest tests |
| `make docker-build` | Build Docker image |
| `make docker-up` | Start services with docker-compose |
| `make docker-down` | Stop services with docker-compose |
| `make clean` | Remove cache and temporary files |

## Data Models

### User Model

```python
{
  "id": int,          # Auto-generated
  "name": str,        # Required, 1-100 characters
  "email": str,       # Required, 1-100 characters
  "age": int | null   # Optional, 0-150
}
```

## Development Notes

- The application uses in-memory storage, so data is not persisted between restarts
- The API automatically validates input using Pydantic models
- Interactive API documentation is available at `/docs` and `/redoc`

## License

This project is licensed under the terms specified in the LICENSE file.
