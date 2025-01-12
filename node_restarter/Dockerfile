FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install pip and set up dependencies
RUN pip install --upgrade pip

# Copy requirements file first to leverage caching for dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port (optional, documents the port)
EXPOSE 6002

# Define the default command
CMD ["python", "app.py"]
