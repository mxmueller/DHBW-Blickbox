FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install Flask==3.0.2 influxdb==5.3.1 gunicorn==21.2.0 flask-sock==0.7.0 redis==4.3.4 docker==7.1.0 flask-cors==5.0.0


CMD ["gunicorn", "-b", "0.0.0.0:5000","--workers", "2", "--threads", "5", "DataBaseAPI:app"]
