FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update
RUN apt-get install build-essential python3-dev default-libmysqlclient-dev -y

# Copy the application code to the container image
RUN mkdir /server
WORKDIR /server

# Install application dependencies
ADD ./requirements.txt /server/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Expose the gRPC port
EXPOSE $PORT

# Copy the program source files
#COPY ./server .

# Compile the gRPC protobuf files
# RUN python -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. todo.proto

# Start the gRPC server
CMD [ "python", "main.py" ]
