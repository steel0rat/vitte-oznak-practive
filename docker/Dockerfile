FROM python:3.13.7

WORKDIR /var/www/practica

COPY ./program .
RUN mkdir -p output

RUN pwd && ls -al && pip install -r requirements.txt && pwd && ls -al && echo 'ok'
