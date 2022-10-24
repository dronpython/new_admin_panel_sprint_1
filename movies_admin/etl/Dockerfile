FROM python:3.8

WORKDIR /usr/app/

VOLUME $HOME/etl_logs:/usr/app/etl/logs

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]