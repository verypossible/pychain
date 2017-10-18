FROM python:3

RUN mkdir /code
WORKDIR /code

RUN pip install pipenv

COPY Pipfile.lock Pipfile /code/
RUN pipenv install --system
