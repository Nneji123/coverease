FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
  wget \
  wkhtmltopdf

RUN pip install --upgrade setuptools 

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . . 

ENV POSTGRES value
ENV SQLITE value
ENV SERVER_MODE value
ENV SERIAL value
ENV OPENAI_KEY value
ENV GOOGLE_OAUTH_CLIENT_ID value
ENV GOOGLE_OAUTH_CLIENT_SECRET value
ENV OAUTHLIB_RELAX_TOKEN_SCOPE value
ENV OAUTHLIB_INSECURE_TRANSPORT value
ENV GITHUB_OAUTH_CLIENT_SECRET value
ENV GITHUB_OAUTH_CLIENT_ID value
ENV ADMIN_USERNAME value
ENV ADMIN_PASSWORD value
ENV ADMIN_EMAIL value
ENV IS_ADMIN value
ENV DEV_MAIL_SERVER value
ENV DEV_MAIL_PORT value
ENV DEV_MAIL_USERNAME value
ENV DEV_MAIL_PASSWORD value
ENV DEV_SECRET_KEY value
ENV DEV_SENDER_EMAIL value
ENV PROD_MAIL_SERVER value
ENV PROD_MAIL_PORT value
ENV PROD_MAIL_USERNAME value
ENV PROD_MAIL_PASSWORD value
ENV PROD_SECRET_KEY value
ENV PROD_SENDER_EMAIL value

RUN cd src && python init.py

CMD gunicorn app:app 