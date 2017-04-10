FROM python:2
RUN apt-get update \
 && apt-get install -yq sqlite \
 && rm -rf /var/lib/apt/lists/*
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
