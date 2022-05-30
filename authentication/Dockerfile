###########
# BUILDER #
###########

# pull official base image
FROM python:3.9.13-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
# RUN apt update && apt upgrade -y
# RUN apt install python3-dev libpq-dev -y
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9.13-slim

# create directory for the app user
# RUN mkdir -p /home/g19

# create the app user
RUN useradd -ms /bin/bash g19

# create the appropriate directories
ENV HOME=/home/g19
ENV APP_HOME=/home/g19/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# 
# RUN pip install --no-cache-dir --upgrade -r $APP_HOME/requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R g19:g19 $APP_HOME

# change to the app user
USER g19

# Run app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
