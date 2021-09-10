FROM python:3.7
LABEL vigicovid.authors="lozanoAlvarez@gmail.com"

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt
COPY /app /app

EXPOSE 8080

CMD [ "python3", "/app/src/run.py"]

