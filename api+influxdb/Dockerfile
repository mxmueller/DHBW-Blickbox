FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install Flask influxdb

# Befehl, der beim Starten des Containers ausgeführt wird
CMD ["python", "DataBaseAPI.py"]
