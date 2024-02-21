from flask import Flask, request, jsonify, make_response
from influxdb import InfluxDBClient
import requests
import socket

app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')

def return_response(message, value, status_code):
    data = {message: value}
    response = make_response(jsonify(data), status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/iot/api/pingBB', methods=['GET'])
def pingBlickBox():
    ip_address = '172.19.80.1'
    port = 22
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  
        s.connect((ip_address, port))
        s.close() 
        return return_response("message", "BlickBox ist erreichbar", 200)
    except Exception as e:
        return return_response("Fehler", "Keine Verbindung zur Blickbox", 503)


@app.route('/iot/api/pingGF', methods=['GET'])
def pingGrafana():
    url = "http://grafana-server:3000/api/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return return_response("message", "Verbingung zu Grafana steht", 200)
        else:
            return return_response("message", "Grafana Server hat geantwortet mit Statuscode {response.status_code}", response.status_code)
    except requests.ConnectionError:
        return return_response("Fehler", "Keine Verbindung zum Grafana Server", 503)



@app.route('/iot/api/pingDB', methods=['GET'])
def pingthis():
    try:
        influx_client.ping()
        return return_response("message", "Verbingung zur Datenbank steht", 200)
    except Exception as e:
        return return_response("error", str(e), 500)



@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    try:
        data = request.json
        if 'temperature' not in data:
            return return_response("message", "Falscher Input!", 400)
        temperature = float(data['temperature'])
        if(temperature < -60.0 or temperature > 100.0):
            return return_response("message", "Falscher Input! Temperatur nicht in Range", 400)
        json_body = [
            {
                "measurement": "temperature",
                "fields": {
                    "value": temperature
                }
            }
        ]
        influx_client.write_points(json_body)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    except Exception as e:
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/air-humidity', methods=['POST'])
def insert_air_humidity():
    try:
        data = request.json
        if 'air-humidity' not in data:
            return return_response("message", "Falscher Input!", 400)
        air_humidity = float(data['air-humidity'])
        if(air_humidity < 0.0 or air_humidity > 100.0):
            return return_response("message", "Falscher Input! Luftfeuchtigkeit nicht in Range", 400)
        json_body = [
            {
                "measurement": "air-humidity",
                "fields": {
                    "value": air_humidity
                }
            }
        ]
        influx_client.write_points(json_body)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        return return_response("error", str(e), 500)

@app.route("/iot/api/insert/rain", methods=['POST'])
def insert_rain_data():
    try:
        data = request.json
        if 'rain' not in data:
            return return_response("message", "Falscher Input!", 400)
        rain = data['rain']
        if(rain < 0 or rain > 3000):
            return return_response("message", "Falscher Input! Regenmenge nicht in Range", 400)
        json_body = [
            {
                "measurement": "rain",
                "fields": {
                    "value": rain
                }
            }
        ]
        influx_client.write_points(json_body)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        return return_response("error", str(e), 500)
    
@app.route("/iot/api/insert/light", methods=['POST'])
def insert_light_data():
    try:
        data = request.json
        if 'light' not in data:
            return return_response("message", "Falscher Input!", 400)
        light = data['light']
        if(light < 0 or light > 1023):
            return return_response("message", "Falscher Input! Lichtmenge nicht in Range", 400)
        json_body = [
            {
                "measurement": "rain",
                "fields": {
                    "value": light
                }
            }
        ]
        influx_client.write_points(json_body)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        return return_response("error", str(e), 500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
