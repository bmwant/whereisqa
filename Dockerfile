# base image
FROM python:3.7.2-slim

# install required libraries
RUN apt-get update && apt-get -y install \
    netcat \
    curl \
    && apt-get clean

# set working directory
WORKDIR /opt/app

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
# use a user
ENV PATH "/root/.poetry/bin:${PATH}"

# add and install requirements
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install

# add entrypoint.sh ?

# bake code in
COPY . /opt/app

# run server
CMD ["poetry", "run", "python", "runserver.py"]
