FROM python:3.11
LABEL authors="junwei"

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages for grpc and environ
RUN pip install grpcio grpcio-tools requests boto3 python-environ protobuf

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Start Server at server.py
CMD ["python", "server.py"]