FROM python:3.9
ADD requirements.txt /
RUN pip3 install -r requirements.txt
ADD main.py /
CMD [ "python", "./main.py" ]