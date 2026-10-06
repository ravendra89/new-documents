# Use the official Python 3.10 image from Docker Hub
FROM python:3.10-slim
RUN apt-get update
RUN apt-get install unzip python3 pip -y
RUN pip install boto3
# Set the working directory inside the container
WORKDIR /app

# Copy your Python code and any requirements.txt to the working directory
COPY script.py /app


# Command to run your Python script when the container starts
CMD ["python", "script.py"]

