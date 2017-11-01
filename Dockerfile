FROM verypossible/serverless:1.20.0-python3

RUN pip install pipenv

COPY Pipfile.lock Pipfile /code/
RUN pipenv install --system
