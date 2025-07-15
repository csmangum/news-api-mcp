# Start with a base Python image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml for dependencies
COPY pyproject.toml /app/

# Install dependencies
RUN pip install uvicorn 'httpx>=0.28.1' 'mcp>=1.1.2' 'python-dotenv>=1.0.0'

# Copy the rest of the application code
COPY src/ /app/src/

# Environment variables will be set at runtime

# Expose the port that the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "-m", "src.news_api_mcp"]
