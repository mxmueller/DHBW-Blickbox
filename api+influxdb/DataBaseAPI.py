from flask import Flask, request, jsonify
from influxdb import InfluxDBClient
import requests
import socket

app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')

@app.route('/iot/api/pingBB', methods=['GET'])
def pingBlickBox():
    ip_address = '172.19.80.1'
    port = 22
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  
        s.connect((ip_address, port))
        s.close() 
        return jsonify({"message": "BlickBox ist erreichbar"}), 200
    except Exception as e:
        return jsonify({"Fehler": "Keine Verbindung zur Blickbox"}), 503



@app.route('/iot/api/pingGF', methods=['GET'])
def pingGrafana():
    url = "http://grafana-server:3000/api/health"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify({"message": "Verbingung zu Grafana steht"}), 200
        else:
            return jsonify({"message": "Grafana Server hat geantwortet mit Statuscode {response.status_code}"}), response.status_code
    except requests.ConnectionError:
        return jsonify({"Fehler": "Keine Verbindung zum Grafana Server"}), 503




@app.route('/iot/api/pingDB', methods=['GET'])
def pingthis():
    try:
        influx_client.ping()
        return jsonify({"message": "Verbingung zur Datenbank steht"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    try:
        data = request.json
        temperature = data['temperature']
        json_body = [
            {
                "measurement": "temperature",
                "fields": {
                    "value": temperature
                }
            }
        ]
        influx_client.write_points(json_body)
        return jsonify({"message": "Daten erfolgreich eingefügt"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
