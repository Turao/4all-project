FROM python:3.7-alpine

ADD . /4all-project/
WORKDIR /4all-project

CMD ["echo", "Installing app dependencies..."]

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN pip install -r requirements.txt
CMD ["echo", "Dependencies installed."]

CMD ["echo", "Container is up and running..."]

WORKDIR /4all-project/src
CMD ["python", "-m" ,"unittest"]
# CMD ["python", "-m" ,"datapoints.hermes"]