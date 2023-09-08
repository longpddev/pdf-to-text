FROM python:latest

RUN apt-get update --fix-missing && apt-get install ocrmypdf -y

WORKDIR /home/extractor
COPY . /home/extractor

RUN pip install -r requirements.txt && mkdir tmp

CMD uvicorn main:app --host 0.0.0.0 --port 8000
EXPOSE 8000