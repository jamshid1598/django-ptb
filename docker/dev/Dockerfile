# pull official base image
FROM python:3.12

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -r backend && useradd -r -g backend backend

RUN mkdir -p /usr/src/backend/media /usr/src/backend/static \
    && chown -R backend:backend /usr/src/backend/

RUN apt-get update && apt-get install -y gdal-bin libgdal-dev libpq-dev && apt-get install -y python3-gdal \
  && apt-get install -y binutils libproj-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy project
COPY . .

RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/backend/entrypoint.sh"]
