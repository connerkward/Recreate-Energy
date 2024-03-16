FROM python:3.9.12-buster
WORKDIR /usr/src/app

RUN apt update
RUN apt install build-essential libssl-dev libffi-dev python-dev cmake -y
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY certificates ./certificates
COPY pi_main.py .
COPY pi_mqtt.py .
COPY pi_serial.py .
COPY pi_localdb.py .

ENTRYPOINT [ "python", "./pi_main.py" ]