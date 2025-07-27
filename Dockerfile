# Use a more stable base image
FROM python:3.9-slim-bullseye

# Install minimal dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || \
    { echo "pip install failed, retrying..."; pip install --no-cache-dir -r requirements.txt; }

# Copy the rest of the application
COPY . .

# Verify critical files exist
RUN echo "Verifying required files:" && \
    ls -la && \
    ls -la data && \
    ls -la components && \
    echo "Requirements:" && \
    pip list
