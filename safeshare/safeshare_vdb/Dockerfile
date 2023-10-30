FROM python:3.11
LABEL authors="junwei"

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages for grpc
RUN pip install grpcio grpcio-tools

# Start Server at server.py
CMD ["python", "server.py"]