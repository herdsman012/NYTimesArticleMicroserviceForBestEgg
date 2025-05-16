# NYTimes Article Microservice

### Prerequisites

- Python 3.12+ installed
- NYTimes Developer API key (obtain from [NYTimes Developer Portal](https://developer.nytimes.com/get-started))
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git https://github.com/herdsman012/NYTimesArticleMicroserviceForBestEgg.git
   cd NYTimesArticleMicroserviceForBestEgg
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

1. **Create an environment file**
   ```bash
   cp .env.sample .env
   ```

2. **Add your NYTimes API key to .env file**
   Open `.env` in your text editor and add your NYTimes API key:
   ```
   NYTIMES_API_KEY=your_api_key_here
   ```

## Running the Application

### Debug Mode

To run the application in debug mode with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

This will start the application on `http://localhost:8000` with auto-reload enabled.

### Release Mode

For release deployment, use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For more robust release deployment, consider using Gunicorn as a process manager:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Note: You would need to install gunicorn first: `pip install gunicorn`

## Testing

### Running Tests

Run all tests with pytest:

```bash
pytest
```

## API Documentation

### Swagger UI

The API includes auto-generated documentation using Swagger UI. Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### 1. Get Top Stories

**Endpoint:** `GET /nytimes/topstories`

Fetches the two most recent top stories from each of the following categories:

- arts
- food
- movies
- travel
- science

**Example Request:**

```bash
curl -X GET "http://localhost:8000/nytimes/topstories"
```

**Example Response:**

```json
{
  "results": [
    {
      "title": "Article Title",
      "section": "arts",
      "url": "https://www.nytimes.com/path/to/article",
      "abstract": "Article abstract text",
      "published_date": "2025-05-01T12:12:-12:12"
    },
    ...
  ],
  "total": 10
}
```

#### 2. Search Articles

**Endpoint:** `GET /nytimes/articlesearch`

Searches for articles using the NYTimes Article Search API.

**Query Parameters:**

- `q` (required): Search query term
- `begin_date` (optional): Begin date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Example Request:**

```bash
curl -X GET "http://localhost:8000/nytimes/articlesearch?q=technology&begin_date=2025-01-01&end_date=2025-05-01"
```

**Example Response:**

```json
{
  "results": [
    {
      "headline": "Article Headline",
      "snippet": "Article snippet text",
      "web_url": "https://www.nytimes.com/path/to/article",
      "pub_date": "2025-05-01T12:12:-12:12"
    },
    ...
  ],
  "total": 42,
  "query": "technology"
}
```

## Troubleshooting

### API Key Issues

If you receive 401 Unauthorized errors:

1. Verify your API key in the `.env` file is correct
2. Check that the `.env` file is in the root directory
3. Ensure the environment variable is loaded properly by adding a print statement in `config.py`

### Connection Issues

If you're having trouble connecting to the NYTimes API:

1. Check your internet connection
2. Verify the NYTimes API endpoints are accessible
3. Check if you've hit your rate limit quota

### Test Failures

If tests are failing:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check that environment variables are correctly set up for testing

For any other issues, please create an issue in the GitHub repository or contact the maintainer.
