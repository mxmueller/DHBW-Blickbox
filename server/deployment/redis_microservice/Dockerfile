FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install redis==4.3.4 docker==7.1.0 websockets==12.0

CMD ["python", "RedisMircoservie.py"]
