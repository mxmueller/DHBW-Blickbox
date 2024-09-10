FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install redis docker websockets

CMD ["python", "RedisMircoservie.py"]
