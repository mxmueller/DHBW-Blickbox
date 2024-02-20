FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install Flask influxdb gunicorn flask-sock

#CMD ["python", "DataBaseAPI.py"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "DataBaseAPI:app"]