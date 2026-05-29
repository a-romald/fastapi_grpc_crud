FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip  && \
    pip install --no-cache-dir -r requirements.txt

#COPY ./app .

# Compile the gRPC protobuf files
# RUN python -m grpc_tools.protoc -I ./protobuf --python_out=. --grpc_python_out=. todo.proto

# Start the FastAPI app
CMD [ "python", "main.py" ]
