

FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /web_django
WORKDIR /web_django
COPY . /web_django/
RUN pip install -r requirements.txt
RUN python manage.py runserver