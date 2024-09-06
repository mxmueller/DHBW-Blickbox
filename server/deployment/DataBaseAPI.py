from flask import Flask, request, jsonify, make_response, url_for
from flask_sock import Sock
from influxdb import InfluxDBClient
import requests
from datetime import datetime
from threading import Lock, Thread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import redis
import docker
from docker.errors import ContainerError, APIError
import os


app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')
redis_client = redis.Redis(host='redis', port=6379, db=0)
sock = Sock(app)
sock.init_app(app)




def redis_listener():
    print("Redis listener started")
    p = redis_client.pubsub()
    p.subscribe(["backend"])
    for message in p.listen():
            if message['type'] == 'message':
                if message['data'] == b'Restart Bitch':
                    print("Restart command received")
                    restart_container()

def restart_container():
    try:
        client = docker.from_env()
        container_id = os.getenv('HOSTNAME')
        container = client.containers.get(container_id)
        container.restart()
        print("Container restarted successfully")
    except ContainerError:
        print("Container not found")
    except APIError as e:
        print(f"Docker API error: {e}")
    except Exception as e:
        print(f"Unexpected error while restarting container: {e}")



def log(title, message, type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {'title': title, 'message': message, 'type': type, 'timestamp': timestamp}
    redis_client.publish("api-logs",json.dumps(log_entry))


def return_response(message, value, status_code):
    data = {message: value}
    response = make_response(jsonify(data), status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

thread_lock = Lock()

@app.route('iot/api/valentin-log', methods=['POST'])
def sendValentinToRedis():
    data = request.json
    redis_client.publish("valentin-logs",json.dumps(data))


@app.route('iot/api/ping', methods=['GET'])
def pingALL():
    onlineGrafana = pingGrafana()
    onlineDatabase = pingBlickBox()
    lastonlineBLickbox = None
    if(onlineDatabase):
        lastonlineBLickbox = pingBlickBox()
    data = {"Grafana-Online" : onlineGrafana, "Database-Online" :  onlineDatabase, "Blickbox-Last-Online": lastonlineBLickbox}
    response = make_response(jsonify(data), 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response




@app.route('/iot/api/pingBB', methods=['POST'])
def insertLastOnline():
    log(title='POST', message=(url_for('insertLastOnline') + " from " + request.remote_addr), type='info')
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    log(title='Try', message='Versuche Zuletzt Online Wert einzufügen', type='info' )
    try:
        timestamp = datetime.now()
        json_body = [
            {
                "measurement": "last_online",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": timestamp.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)


def pingBlickBox():
    log(title='GET', message=(url_for('pingBlickBox') + " from " + request.remote_addr), type='info' )
    log(title='Try', message='Versuche den zuletzt Online Wert der Blickbox abzurufen', type='info' )
    try:
        query = 'SELECT last("value") FROM "last_online"'
        result = influx_client.query(query)
        last_online_value = list(result.get_points())[0]['last']
        log(title='Info', message=f'Zuletzt Online Wert der Blickbox abgerufen: {last_online_value}', type='success' )
        return last_online_value
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return None


def pingGrafana():
    url = "http://grafana-server:3000/api/health"
    log(title='GET', message=(url_for('pingGrafana') + " from " + request.remote_addr), type='info' )
    log(title='Try', message='Versuche Verbindung mit Grafana herzusetellen', type='info' )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            log(title='Connected', message='Verbindung zu Grafana hergestellt', type='success' )
            return True
        else:
            log(title='Info', message=f'Grafana Server hat geantwortet mit Statuscode {response.status_code}', type='info' )
            return False
    except requests.ConnectionError:
        log(title='Keine Verbindung', message='Keine Verbindung zum Grafana Server', type='error' )
        return False



def pingDB():
    log(title='GET', message=(url_for('pingthis') + " from " + request.remote_addr), type='info' )
    log(title='Try', message='Versuche Verbindung zur Datenbank herzusetellen', type='info' )
    try:
        influx_client.ping()
        log(title='Connected', message='Verbindung zur Datenbank hergestellt', type='success' )
        return True
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return False



@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    log(title='POST', message=(url_for('insert_temperature') + " from " + request.remote_addr), type='info' )
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    
    log(title='Try', message='Versuche Temperatur-Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'temperature' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [temperature]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        temperature = float(data['temperature'])
        if(temperature < -40.0 or temperature > 65.0):
            log(title='Exception', message=f'Wert der Temperatur stimmt nicht. Wert: {temperature}', type='error' )
            return return_response("message", "Falscher Input! Temperatur nicht in Range", 400)
        Warning(temperature, "temperature", 35.0, "Achtung sehr heiß", f'Pass auf, die Außentemperatur beträgt {temperature} Grad.')
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
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/air-humidity', methods=['POST'])
def insert_air_humidity():
    log(title='POST', message=(url_for('insert_air_humidity') + " from " + request.remote_addr), type='info' )
    
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    
    log(title='Try', message='Versuche Luftfeuchtigkeits-Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'air_humidity' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [air_humidity]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        air_humidity = float(data['air_humidity'])
        if(air_humidity < 0.0 or air_humidity > 100.0):
            log(title='Exception', message=f'Wert der Luftfeuchtigkeit stimmt nicht. Wert: {air_humidity}', type='error' )
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
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/wind-direction', methods=['POST'])
def insert_wind_direction():
    log(title='POST', message=(url_for('insert_wind_direction') + " from " + request.remote_addr), type='info' )
    
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    
    log(title='Try', message='Versuche Windrichtungs-Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'wind_direction' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [wind_direction]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        
        wind_direction = float(data['wind_direction'])

        if(wind_direction < 0.0 or wind_direction > 360.0):
            log(title='Exception', message=f'Wert der Windrichtung stimmt nicht. Wert: {wind_direction}', type='error' )
            return return_response("message", "Falscher Input! Windrichtungs Wert nicht in Range", 400)
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
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/wind-speed', methods=['POST'])
def insert_wind_speed():
    log(title='POST', message=(url_for('insert_wind_speed') + " from " + request.remote_addr), type='info' )
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    log(title='Try', message='Versuche Windgeschwindigkeits-Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'wind_speed' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [wind_speed]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        wind_speed = float(data['wind_speed'])
        if(wind_speed < 0.0 or wind_speed > 200.0):
            log(title='Exception', message=f'Wert der Windgeschwindigkeit stimmt nicht. Wert: {wind_speed}', type='error' )
            return return_response("message", "Falscher Input! Windgeschwindigkeit nicht in Range", 400)
        Warning(wind_speed, "wind_speed", 60, "Achtung Windig", f'Die Windgeschwindigkeit beträgt {wind_speed} km/h')
        json_body = [
            {
                "measurement": "wind_speed",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": wind_speed
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)

@app.route('/iot/api/insert/rain', methods=['POST'])
def insert_rain():
    log(title='POST', message=(url_for('insert_rain') + " from " + request.remote_addr), type='info' )
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    log(title='Try', message='Versuche Niederschlags-Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'rain' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [rain]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        rain = float(data['rain'])
        if(rain < 0.0 or rain > 1100.0):
            log(title='Exception', message=f'Wert des Niederschlags stimmt nicht. Wert: {rain}', type='error' )
            return return_response("message", "Falscher Input! Niederschlag nicht in Range", 400)
        Warning(rain, "rain", 100, "Regen", "Wie du wahrscheinlich schon draußen siehst, regnet es.")
        json_body = [
            {
                "measurement": "rain",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": rain
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)
    
@app.route('/iot/api/insert/battery-charge', methods=['POST'])
def insert_battery_charge():
    log(title='POST', message=(url_for('insert_battery_charge') + " from " + request.remote_addr), type='info' )
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    log(title='Try', message='Versuche Akkustand Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'battery_charge' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [battery_charge]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        battery_charge = float(data['battery_charge'])
        if(battery_charge < 0.0 or battery_charge > 100.0):
            log(title='Exception', message=f'Wert der Akkustand Wert stimmt nicht. Wert: {battery_charge}', type='error' )
            return return_response("message", "Falscher Input! Akkustands Wert nicht in Range", 400)
        
        Warning((100.0-battery_charge), "battery_charge", 70, "Akku fast leer!", "Der Akku der Blickbox ist bei 30%")

        json_body = [
            {
                "measurement": "battery_charge",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": battery_charge
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)


@app.route('/iot/api/insert/battery-voltage', methods=['POST'])
def insert_battery_voltage():
    log(title='POST', message=(url_for('insert_battery_voltage') + " from " + request.remote_addr), type='info' )
    if request.headers.get('blickbox') != 'true':
        log(title='Exception', message='Unauthorized acess detected!', type='error' )
        return return_response("error", "Unauthorized", 401)
    log(title='Try', message='Versuche Batteriespannungs Wert einzufügen', type='info' )
    try:
        data = request.json
        if 'timestamp' in data:
            timestamp = data['timestamp']
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                log(title='Exception', message=f'Timestamp-Wert stimmt nicht. Wert: {timestamp}', type='error' )
                return return_response("message", "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'", 400)
        else:
            timestamp = datetime.now()

        if 'battery_voltage' not in data:
            log(title='Exception', message="Key der Eingabe war nicht [battery_voltage]", type='error' )
            return return_response("message", "Falscher Input!", 400)
        battery_voltage = float(data['battery_voltage'])
        if(battery_voltage < 0.0 or battery_voltage > 4.5):
            log(title='Exception', message=f'Wert der Batteriespannungs Wert stimmt nicht. Wert: {battery_voltage}', type='error' )
            return return_response("message", "Falscher Input! Batteriespannungs Wert nicht in Range", 400)
        json_body = [
            {
                "measurement": "battery_voltage",
                "time": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fields": {
                    "value": battery_voltage
                }
            }
        ]
        influx_client.write_points(json_body)
        log(title='Info', message='Daten wurden erfolgreich eingefügt!', type='success' )
        return return_response("message", "Daten erfolgreich eingefügt!", 200)
    
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )
        return return_response("error", str(e), 500)



def Warning(value, measurement, limit, subject, message):
    try:
        query = f'SELECT last("value") FROM "{measurement}"'
        result = influx_client.query(query)
        last_value = list(result.get_points())[0]['last']
        if(measurement == "battery_charge"):
            last_value = 100.0 - last_value
            
        if(value > limit and last_value < limit):
            sendEmail(subject, message)
    except Exception as e:
        error = str(e).replace('"', '').replace("'", "")
        log(title='Exception', message=error, type='error' )


def sendEmail(subject, body):
    query = f'SELECT last("value") FROM "emailpw"'
    result = influx_client.query(query)
    password =str(list(result.get_points())[0]['last'])
    senderEmail = 'blickbox@maytastix.de'
    receiver_email = 'aronseidl17@gmail.com'

    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.strato.de", 587) as server:  
        server.starttls()
        server.login(senderEmail, password)
        server.sendmail(senderEmail, receiver_email, message.as_string())

redis_thread = Thread(target=redis_listener)
redis_thread.daemon = True
redis_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


