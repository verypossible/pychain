FROM python:3

RUN pip install \
        flask \
        psycopg2 \
        redis \
        sqlalchemy


RUN mkdir /code
WORKDIR /code
