FROM python:3.9-slim
WORKDIR /app
RUN pip install flake8 requests
