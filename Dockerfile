# Use a Python base image
FROM python:3.9-slim

# Install system dependencies for gcloud and kubectl
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud CLI and gke-gcloud-auth-plugin
RUN curl -sSL https://sdk.cloud.google.com | bash -s -- --install-dir=/usr/local/gcloud --disable-prompts

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl \
    && mv ./kubectl /usr/local/bin/kubectl

# Add gcloud and kubectl to the PATH
ENV PATH="/usr/local/gcloud/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .
