# Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=user_directory.settings

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --find-links=/wheels -r requirements.txt && \
    pip install drf-yasg==1.21.7

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/static /app/logs && \
    chmod 777 /app/logs

# Copy wait-for-it.sh and make it executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Print installed packages for debugging
RUN pip freeze

# Remove or properly set PYTHONPATH if needed
# ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages:$PYTHONPATH

CMD ["gunicorn", "user_directory.wsgi:application", "--bind", "0.0.0.0:8000"]
