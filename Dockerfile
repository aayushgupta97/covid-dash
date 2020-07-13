FROM python:3.7.0-alpine3.8

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps build-base gcc musl-dev libffi-dev py-cffi openssl-dev python-dev libxml2-dev libxslt-dev
RUN pip install cython
RUN pip install -r requirements.txt

COPY . . 

CMD python run.py