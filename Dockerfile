FROM verypossible/serverless:1.23-python3

RUN pip install pipenv

COPY Pipfile.lock Pipfile /code/
RUN pipenv install --system
