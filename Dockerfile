# Use a lightweight official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container first to optimize caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the pipeline code into the container
COPY . /app

# If your pipeline needs to be executed by a specific command, define it here.
# The Cloud Build step will override this with 'python pipeline.py'
