FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD python3 start.py