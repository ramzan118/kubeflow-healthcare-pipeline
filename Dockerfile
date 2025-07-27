# Use a smaller base image
FROM python:3.9-slim-bullseye

# Install essential build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with retries
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "Retrying pip install..." && sleep 5 && pip install --no-cache-dir -r requirements.txt) || \
    (echo "Second retry..." && sleep 10 && pip install --no-cache-dir -r requirements.txt)

# Copy application files
COPY . .

# Verify critical files exist
RUN echo "Verifying required files:" && \
    ls -la && \
    [ -f requirements.txt ] && \
    [ -f pipeline.py ] && \
    [ -d components ] && \
    [ -f data/patients.csv ] && \
    echo "All required files present" || \
    (echo "Missing required files!"; exit 1)

# Set a neutral entrypoint
ENTRYPOINT ["python3"]
