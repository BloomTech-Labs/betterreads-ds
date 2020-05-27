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
RUN wget https://elasticbeanstalk-us-east-1-394688380943.s3.amazonaws.com/compressed_sim_matrix.zip
RUN unzip \*.zip
RUN rm *.zip
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python3"]

CMD ["gunicorn_entrypoint.py"]
