# Use the official Python 3.12 image from the Docker Hub
FROM pytorch/pytorch:2.6.0

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY main.py /app/
COPY api/ /app/api/
COPY setup.py /app/
COPY train.zip /app/
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the application
ENTRYPOINT ["sh", "-c", "sleep 20 && python setup.py && sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]