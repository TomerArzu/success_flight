#FROM ubuntu
FROM python:3.10-slim-buster

WORKDIR /opt/success_flight

RUN apt-get update
RUN mkdir -p /opt/success_fligt
COPY . /opt/success_flight

#RUN apt-get install -y python && apt-get install -y pip
#RUN pip install flask

RUN pip install -r /opt/success_flight/requirements.txt


EXPOSE 5000

ENTRYPOINT FLASK_APP=/opt/success_flight/app.py flask run --host=0.0.0.0 --port 5000