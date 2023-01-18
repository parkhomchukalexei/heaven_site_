

FROM python:3.10
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
COPY . /web_django/
WORKDIR /web_django
RUN pip install -r requirements.txt
RUN adduser --disabled-password admin-user

USER admin-user