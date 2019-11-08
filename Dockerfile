FROM circleci/python:3.7.2-stretch-browsers AS base
WORKDIR /app
COPY requirements.txt .
RUN sudo mkdir /app/staticfiles
RUN sudo pip install -r requirements.txt
RUN sudo pip install honcho

FROM base AS service
WORKDIR /app
COPY . .
