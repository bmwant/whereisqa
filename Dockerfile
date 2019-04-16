# base image
FROM python:3.7.2-slim

# install required libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat \
    curl \
    && apt-get clean

# install node
WORKDIR /opt
RUN curl -sL https://deb.nodesource.com/setup_11.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh

# install Node.js 11.x and npm
RUN apt-get install -y \
    nodejs

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
# use a user
ENV PATH "/root/.poetry/bin:${PATH}"

# set working directory
WORKDIR /opt/app

# add and install js requirements
COPY package.json .
COPY package-lock.json .
RUN npm install

# add and install python requirements
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install

# bake code in
COPY . /opt/app

# run server
CMD ["poetry", "run", "python", "runserver.py"]
