FROM python:3.14.2-slim

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY source/. .

CMD ["sh", "-c", "python main.py"]
