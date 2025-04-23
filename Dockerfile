FROM python:3.13-slim

WORKDIR /app

# Copy dependency files first for better caching
COPY python_adk/requirements.txt python_adk/pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

# Expose port
EXPOSE 10000

# Run with gunicorn and uvicorn workers
CMD ["gunicorn", "python_adk.asgi:application", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:10000"] 