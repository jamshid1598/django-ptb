###########
# BUILDER #
###########

# pull official base image
FROM python:3.12 as builder

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/backend/
# RUN flake8 --ignore=E501,F401,E731,F403,E126,F841,E127,F405,E117,W503,W504,E123,E402 .

# install python dependencies
COPY ./requirements.txt /requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/backend/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.12

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static_root
RUN mkdir $APP_HOME/media_root
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
   && apt-get install -y --no-install-recommends apt-utils && apt-get install -y gettext
RUN apt-get update && apt-get install -y iputils-ping && apt-get install -y redis-tools
COPY --from=builder /usr/src/backend/wheels /wheels
COPY --from=builder /usr/src/backend/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
# RUN chown -R app:app $APP_HOME

# fix permissions
# RUN chmod -R 755 $APP_HOME

# change to the app user
# USER app

# run entrypoint.prod.sh
ENTRYPOINT ["sh", "/home/app/backend/entrypoint.sh"]
