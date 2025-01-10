# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Create the curl_logs.txt file
RUN touch curl_logs.txt

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt .

# RUN pip install -r requirements.txt
# Install any needed dependencies specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run the app.py file when the container launches
CMD ["python", "script.py"]
