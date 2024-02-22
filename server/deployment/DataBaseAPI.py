from flask import Flask, request, jsonify, make_response, url_for
from flask_sock import Sock
from influxdb import InfluxDBClient
import requests
import socket
import time
from RingBuffer import *
from threading import Lock

app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')
sock = Sock(app)
sock.init_app(app)

ringBuffer = RingBuffer(10)

def return_response(message, value, status_code):
    data = {message: value}
    response = make_response(jsonify(data), status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

thread_lock = Lock()

@sock.route('/log-stream')
def logstream(sock):
    try:
        while True:
            with thread_lock:
                check_and_send_new_entries(ringBuffer, sock)
    except Exception as e:
        print('Socket-Verbindung unterbrochen:', e)
        sock.close()


@app.route('/iot/api/pingBB', methods=['GET'])
def pingBlickBox():
    ip_address = '172.19.80.1'
    port = 22
    log(title='GET', message=(url_for('pingBlickBox') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Versuch', message='Versuche Verbindung zur Blickbox herzusetellen', type='info', ringbuffer=ringBuffer)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  
        s.connect((ip_address, port))
        s.close() 
        log(title='Connected', message='Verbindung zur BlickBox hergestellt', type='success', ringbuffer=ringBuffer)
        return return_response("message", "BlickBox ist erreichbar", 200)
    except Exception as e:
        log(title='Keine Verbindung', message='Keine Verbindung zur Blickbox', type='error', ringbuffer=ringBuffer)
        return return_response("Fehler", "Keine Verbindung zur Blickbox", 503)


@app.route('/iot/api/pingGF', methods=['GET'])
def pingGrafana():
    url = "http://grafana-server:3000/api/health"
    log(title='GET', message=(url_for('pingGrafana') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Versuch', message='Versuche Verbindung mit Grafana herzusetellen', type='info', ringbuffer=ringBuffer)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            log(title='Connected', message='Verbindung zu Grafana hergestellt', type='success', ringbuffer=ringBuffer)
            return return_response("message", "Verbingung zu Grafana steht", 200)
        else:
            log(title='Info', message=f'Grafana Server hat geantwortet mit Statuscode {response.status_code}', type='info', ringbuffer=ringBuffer)
            return return_response("message", f'Grafana Server hat geantwortet mit Statuscode {response.status_code}', response.status_code)
    except requests.ConnectionError:
        log(title='Keine Verbindung', message='Keine Verbindung zum Grafana Server', type='error', ringbuffer=ringBuffer)
        return return_response("Fehler", "Keine Verbindung zum Grafana Server", 503)



@app.route('/iot/api/pingDB', methods=['GET'])
def pingthis():
    log(title='GET', message=(url_for('pingthis') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Versuch', message='Versuche Verbindung zur Datenbank herzusetellen', type='info', ringbuffer=ringBuffer)

    try:
        influx_client.ping()
        log(title='Connected', message='Verbindung zur Datenbank hergestellt', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Verbingung zur Datenbank steht", 200)
    except Exception as e:
        log(title='Exception', message=str(e), type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)



@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    log(title='POST', message=(url_for('insert_temperature') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Versuch', message='Versuche Temperatur-Wert einzufügen', type='info', ringbuffer=ringBuffer)
    try:
        data = request.json
        if 'temperature' not in data:
            log(title='Exception', message="Key der Eingabe war nicht 'temperature'", type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input!", 400)
        temperature = float(data['temperature'])
        if(temperature < -60.0 or temperature > 100.0):
            log(title='Exception', message=f'Wert der Temperatur stimmt nicht. Wert: {temperature}', type='error', ringbuffer=ringBuffer)
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
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    except Exception as e:
        log(title='Exception', message=str(e), type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
