FROM python
ADD requirements.txt /
RUN python -m pip install --upgrade pip
#RUN pip install -r requirements.txt
ADD main.py /
CMD [ "python", "./main.py" ]