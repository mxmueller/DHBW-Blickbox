from flask import Flask, request, jsonify, make_response
from flask_sock import Sock
from influxdb import InfluxDBClient
import requests
import socket

app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')
sock = Sock(app)
sock.init_app(app)


@sock.route('/log-stream')
def logstream(ws):
    while True:
        data = ws.receive()
        ws.send(data)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
