FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
  wget \
  wkhtmltopdf

RUN pip install --upgrade setuptools 

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . . 

RUN cd src && python init.py

CMD gunicorn app:app 