FROM python:3.10.5
#FROM gorialis/discord.py

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD [ "python3", "./main.py" ]