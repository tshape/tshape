FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR ./app
ADD . /app/
ADD requirements_dev.txt /app/
RUN pip3 install -r requirements_dev.txt
WORKDIR ./src
