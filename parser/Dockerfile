FROM python:3.10-alpine

WORKDIR /app

COPY . /app
RUN pip3 install -r /app/requirements.txt

COPY crontab /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN crontab -l

CMD [ "/usr/sbin/crond", "-f" ]