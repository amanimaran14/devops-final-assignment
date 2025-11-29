FROM python:3.9-slim

WORKDIR /var/jenkins_home/workspace/Code-Quality-Checker-Project

COPY . .

RUN pip install flake8 requests

