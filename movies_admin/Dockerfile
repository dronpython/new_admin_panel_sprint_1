FROM python:3.8

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["config.wsgi", "-b", "0.0.0.0:8000"]