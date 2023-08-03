FROM python:3.10.5
FROM gorialis/discord.py

RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD [ "python3", "./main.py" ]