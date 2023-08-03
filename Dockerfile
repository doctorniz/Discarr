FROM python:3.10.5
FROM gorialis/discord.py

RUN pip install --upgrade -y pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r -y requirements.txt

COPY . .
CMD [ "python3", "./main.py" ]