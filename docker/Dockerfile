# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ../app/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ../app .

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Define the command to run the FastAPI application
ENTRYPOINT ["python", "main.py"]