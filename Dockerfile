# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . /code/

# Create necessary directories
RUN mkdir -p /code/staticfiles /code/static

# Collect static files
RUN python manage.py collectstatic --noinput

# Make entrypoint.sh executable
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
