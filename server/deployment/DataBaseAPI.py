from flask import Flask, request, jsonify, make_response, url_for
from flask_sock import Sock
from influxdb import InfluxDBClient
import requests
import socket
from datetime import datetime
import time
from RingBuffer import *
from threading import Lock


app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')
sock = Sock(app)
sock.init_app(app)

ringBuffer = RingBuffer(30)

def return_response(message, value, status_code):
    data = {message: value}
    response = make_response(jsonify(data), status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


  

@app.route('/iot/api/getBBIP', methods=['GET'])
def getBBIP():
    global ip_adress
    ip_adress = request.remote_addr
    return return_response('message', f'IP-Adresse der BlickBox geupdatet. Neue IP: {ip_adress}', 200)


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
    #global ip_adress
    if(not ip_adress):
        return return_response("message", "IP-Adresse der Blickbox nicht gefunden!", 503)
    port = 22
    log(title='GET', message=(url_for('pingBlickBox') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Try', message='Versuche Verbindung zur Blickbox herzusetellen', type='info', ringbuffer=ringBuffer)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  
        s.connect((ip_adress, port))
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
    log(title='Try', message='Versuche Verbindung mit Grafana herzusetellen', type='info', ringbuffer=ringBuffer)
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
    log(title='Try', message='Versuche Verbindung zur Datenbank herzusetellen', type='info', ringbuffer=ringBuffer)

    try:
        influx_client.ping()
        log(title='Connected', message='Verbindung zur Datenbank hergestellt', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Verbingung zur Datenbank steht", 200)
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)



@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    log(title='POST', message=(url_for('insert_temperature') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Try', message='Versuche Temperatur-Wert einzufügen', type='info', ringbuffer=ringBuffer)
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error', ringbuffer=ringBuffer)
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'temperature' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [temperature]", type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input!", 400)
        temperature = float(data['temperature'])
        if(temperature < -60.0 or temperature > 100.0):
            log(title='Exception', message=f'Wert der Temperatur stimmt nicht. Wert: {temperature}', type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input! Temperatur nicht in Range", 400)
        json_body = [
            {
                "measurement": "temperature",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": temperature
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/air-humidity', methods=['POST'])
def insert_air_humidity():
    log(title='POST', message=(url_for('insert_air_humidity') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Try', message='Versuche Luftfeuchtigkeits-Wert einzufügen', type='info', ringbuffer=ringBuffer)
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error', ringbuffer=ringBuffer)
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'air_humidity' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [air_humidity]", type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input!", 400)
        air_humidity = float(data['air_humidity'])
        if(air_humidity < 0.0 or air_humidity > 100.0):
            log(title='Exception', message=f'Wert der Luftfeuchtigkeit stimmt nicht. Wert: {air_humidity}', type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input! Luftfeuchtigkeit nicht in Range", 400)
        json_body = [
            {
                "measurement": "air_humidity",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": air_humidity
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/wind_direction', methods=['POST'])
def insert_wind_direction():
    log(title='POST', message=(url_for('insert_wind_direction') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Try', message='Versuche Windrichtungs-Wert einzufügen', type='info', ringbuffer=ringBuffer)
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error', ringbuffer=ringBuffer)
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'wind_direction' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [wind_direction]", type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input!", 400)
        wind_direction = data['wind_direction']
        json_body = [
            {
                "measurement": "wind_direction",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": wind_direction
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/wind-speed', methods=['POST'])
def insert_wind_speed():
    log(title='POST', message=(url_for('insert_wind_speed') + " from " + request.remote_addr), type='info', ringbuffer=ringBuffer)
    log(title='Try', message='Versuche Windgeschwindigkeits-Wert einzufügen', type='info', ringbuffer=ringBuffer)
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error', ringbuffer=ringBuffer)
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'wind-speed' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [wind_speed]", type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input!", 400)
        wind_speed = float(data['wind-speed'])
        if(wind_speed < 0.0 or wind_speed > 500.0):
            log(title='Exception', message=f'Wert der Windgeschwindigkeit stimmt nicht. Wert: {wind_speed}', type='error', ringbuffer=ringBuffer)
            return return_response("message", "Falscher Input! Windgeschwindigkeit nicht in Range", 400)
        json_body = [
            {
                "measurement": "wind-speed",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": wind_speed
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success', ringbuffer=ringBuffer)
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error', ringbuffer=ringBuffer)
        return return_response("error", str(e), 500)

#@app.route("/iot/api/insert/rain", methods=['POST'])
#def insert_rain_data():
#    try:
#        data = request.json
#        if 'rain' not in data:
#            return return_response("message", "Falscher Input!", 400)
#        rain = data['rain']
#        if(rain < 0 or rain > 3000):
#            return return_response("message", "Falscher Input! Regenmenge nicht in Range", 400)
#        json_body = [
#            {
#                "measurement": "rain",
#                "fields": {
#                    "value": rain
#                }
#            }
#        ]
#        influx_client.write_points(json_body)
#        return return_response("message", "Daten erfolgreich eingefügt!", 200)
#    
#    except Exception as e:
#        return return_response("error", str(e), 500)
    
#@app.route("/iot/api/insert/light", methods=['POST'])
#def insert_light_data():
#    try:
#        data = request.json
#        if 'light' not in data:
#            return return_response("message", "Falscher Input!", 400)
#        light = data['light']
#        if(light < 0 or light > 1023):
#            return return_response("message", "Falscher Input! Lichtmenge nicht in Range", 400)
#        json_body = [
#            {
#                "measurement": "rain",
#                "fields": {
#                    "value": light
#                }
#            }
#        ]
#        influx_client.write_points(json_body)
#        return return_response("message", "Daten erfolgreich eingefügt!", 200)
#    
#    except Exception as e:
#        return return_response("error", str(e), 500)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
