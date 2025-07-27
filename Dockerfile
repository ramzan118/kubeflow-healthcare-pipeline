FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud CLI
RUN curl -sSL https://sdk.cloud.google.com > /tmp/gcloud_install.sh \
    && bash /tmp/gcloud_install.sh --install-dir=/usr/local/gcloud --disable-prompts \
    && rm /tmp/gcloud_install.sh

# Install kubectl and gke-gcloud-auth-plugin
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# Add gcloud to PATH
ENV PATH $PATH:/usr/local/gcloud/bin

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
