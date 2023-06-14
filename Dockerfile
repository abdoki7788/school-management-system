FROM python:3.8-alpine

WORKDIR /src

COPY requirements.txt /src/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD [ "gunicorn", "config.wsgi", ":8000" ]