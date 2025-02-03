# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy required files
COPY requirements.txt .
COPY spotisync.py .
COPY client_secret.json .
COPY .env .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for OAuth authentication
EXPOSE 8080

# Set the default command to run the script
CMD ["python", "spotisync.py"]