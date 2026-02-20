# Use Python 3.12 slim image (stable and compatible)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Debug: Check Python version
RUN python --version && which python

# Copy dependency files
# Only copy pyproject.toml, not uv.lock, to avoid Python version conflicts
COPY pyproject.toml ./

# Install dependencies
# uv will resolve dependencies for the current Python version
RUN uv sync

# Copy application code
COPY main.py ./

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["uv", "run", "python", "main.py"]