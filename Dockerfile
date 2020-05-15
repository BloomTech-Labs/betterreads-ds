FROM ubuntu:18.04

### For reliable logging/io
ENV PYTHONBUFFERED=1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip python3-dev unzip

RUN mkdir /app
### Copy requirements first to leverage cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

WORKDIR /app/readrr_api/route_tools
RUN unzip nlp.zip && unzip nn.zip && unzip tfidf_model.zip
WORKDIR /app

ENTRYPOINT ["python3"]

CMD ["gunicorn_entrypoint.py"]
