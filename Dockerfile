FROM python:2-onbuild
RUN apt-get update && apt-get install -yq sqlite
CMD python voting.py
