# Use a lightweight official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pipeline code and dependencies into the container
COPY . /app

# If your pipeline has dependencies, list them in a requirements.txt file
# and install them here.
# For example:
# RUN pip install --no-cache-dir -r requirements.txt

# If your pipeline needs to be executed by a specific command, define it here.
# The Cloud Build step will override this with 'python pipeline.py'
