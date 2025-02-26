# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory inside the container
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy only requirements file first (to optimize Docker caching)
COPY requirements.txt .

# Install dependencies as root
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN adduser --system --group --disabled-password appuser
USER appuser

# Copy the rest of the application files
COPY . ./

# Expose the required port (Cloud Run automatically sets the PORT variable)
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD curl --fail http://localhost:$PORT/ || exit 1

# Start the application using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
