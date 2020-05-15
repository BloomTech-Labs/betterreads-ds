FROM python:3.6

### For reliable logging/io
ENV PYTHONBUFFERED=1


RUN mkdir /app
### Copy requirements first to leverage cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app/readrr_api/route_tools
RUN unzip nlp.zip && unzip nn.zip && unzip tfidf_model.zip
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python3"]

CMD ["gunicorn_entrypoint.py"]
