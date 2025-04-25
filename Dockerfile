FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY . .

# Expose the port the application runs on
EXPOSE 8000

# Create a non-root user and change ownership
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Command to run the application
CMD ["python", "main.py"]