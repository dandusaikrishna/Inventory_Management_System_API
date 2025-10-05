# syntax=docker/dockerfile:1

# Build stage
FROM python:3.11-slim as builder

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r production.txt

# Final stage
FROM python:3.11-slim

# Create app user
RUN useradd -ms /bin/bash app

# Create directory for the app user
WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/production.txt .

# Install dependencies
RUN pip install --no-cache /wheels/*

# Copy project
COPY . .

# Set ownership
RUN chown -R app:app /app

# Switch to app user
USER app

# Run script
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]