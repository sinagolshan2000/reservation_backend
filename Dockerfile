# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
# We install postgresql-client to use pg_isready
RUN apt-get update \
    && apt-get -y install netcat-traditional postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple


# Copy project
COPY . /app/

# Add a script to wait for the database to be ready
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
