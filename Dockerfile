FROM python:3.9-slim

WORKDIR /usr/src/app

# Copy all repo files into the container image
COPY . .

RUN pip install flake8 requests

