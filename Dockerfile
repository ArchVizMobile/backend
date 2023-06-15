FROM python:3.11-slim-buster
WORKDIR /archviz

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["python3", "main.py"]