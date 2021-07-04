# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/PAS_app/requirements.txt
RUN pip install -r ./PAS_app/requirements.txt

# copy project
COPY ./env.dev ./
COPY ./entrypoint.sh ./entrypoint.sh

COPY . /usr/src/PAS_app/
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]