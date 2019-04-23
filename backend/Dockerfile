FROM python:2.7

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get -y install cron
ADD crontab /etc/cron.d/extract
RUN chmod 0644 /etc/cron.d/extract
RUN crontab /etc/cron.d/extract
RUN touch /var/log/extract

CMD cron && python app/timelines.py
