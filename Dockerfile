FROM tiangolo/uwsgi-nginx:python3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install python-dev postgresql-client libssl-dev -y
RUN mkdir /code
WORKDIR /code
COPY src /code/

ENTRYPOINT ["python","./pizzabot.py"]
