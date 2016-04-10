FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip3 install -r requirements.txt
ADD . /app/
