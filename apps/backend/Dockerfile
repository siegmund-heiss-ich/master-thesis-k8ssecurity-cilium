# Use an official Python runtime as a parent image
FROM python:3.12.5-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./apps/backend/backend.py /app
COPY ./apps/backend/requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000
EXPOSE 8080

# Start both uvicorn servers on different ports
CMD ["sh", "-c", "uvicorn backend:app --host 0.0.0.0 --port 5000 & uvicorn backend:app --host 0.0.0.0 --port 8080"]