FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

CMD [ "python3", "main.py" ]