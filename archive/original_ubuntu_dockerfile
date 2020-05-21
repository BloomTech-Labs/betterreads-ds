FROM ubuntu:18.04

### For reliable logging/io
ENV PYTHONBUFFERED=1
RUN apt-get update && \
    apt-get upgrade -y && \ 
    apt-get install -y python3-pip python3-dev

RUN mkdir /app
### Copy requirements first to leverage cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn"]

CMD ["-b", "0.0.0.0:8000", "application:app"]
