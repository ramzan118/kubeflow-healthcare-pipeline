FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Verify critical files exist
RUN echo "Verifying required files:" && \
    ls -la && \
    [ -f data/patients.csv ] && \
    [ -f pipeline.py ] && \
    [ -f components/process_data.py ] && \
    echo "All required files present"
