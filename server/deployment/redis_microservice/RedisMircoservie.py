import redis
import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import websockets
import os
from datetime import datetime, timedelta

# Online Status der Komponenten
onlinestatus = {
                "Valentin-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "Grafana-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "Database-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "ADA-Online": {"online" : False, "timestamp" : "1970-1-1 00:00:00"},
                "SARA-Online": {"online" : False, "timestamp" : "1970-1-1 00:00:00"}
                }

# Umgebungsvariablen die Wichtig sind
link = os.getenv("EMAIL_SMTP_SERVER")
port = os.getenv("EMAIL_SMTP_PORT")
password = os.getenv("EMAIL_SMTP_PASSWORD")



r = redis.Redis(host='redis', port=6379, db=0)                                                          # Verbindung zur Redis-Datenbank
p = r.pubsub()                                                                                          # Publisher/Subscriber System von Redis
logging.getLogger('websockets').setLevel(logging.ERROR)                                                 # Fehler aus der Websocket Libary werden unterdrückt (es sollen nur unsere Logs angezeigt werden)
logging.getLogger('asyncio').setLevel(logging.ERROR)                                                    # Fehler aus der AsyncIO Libary werden unterdrückt   (es sollen nur unsere Logs angezeigt werden)
logging.basicConfig(filename='./logdaten/system_logs.log', level=logging.INFO)                          # Logs werden zusätzlich in ein Log-File geschrieben

p.subscribe(["api-logs", "valentin-logs", "grafana-logs", "ada-logs", "sara-logs", "influx-logs"])      # Die Channel der Jeweiligen Komponenten im Gesamt-System

publisherList = ["backend","valentin",  "ada", "sara", "grafana", "influx"]                             # Die Channel über die Online und Restart Abfragen gemacht werden


connected_clients = []                                                                                  # Offene Frontend Connections
onlinestatus_connected_clients = []                                                                     # Offene Frontend Connections

# Eingehende Verbindungen werden in die Liste geschrieben & Eingehende Nachrichten werden Ignoriert (nur der Microservice Sendet)
async def websocket_server(websocket, path):
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            pass  
    finally:
        connected_clients.remove(websocket)

# Eingehende Verbindungen werden in die Liste geschrieben & Eingehende Nachrichten werden Ignoriert (nur der Microservice Sendet)
async def onlinestatus_server(websocket, path):
    onlinestatus_connected_clients.append(websocket)
    try:
        async for message in websocket:
            pass  
    finally:
        onlinestatus_connected_clients.remove(websocket)

# Main Funktion
async def redis_listener():
    start_server = websockets.serve(websocket_server, "0.0.0.0", 5001)                          # Websocket für die Logs wird geöffnet
    await start_server
    onlinestatus_start_server = websockets.serve(onlinestatus_server, "0.0.0.0", 5002)          # Websocket für die zuletzt Online Daten wird geöffnet
    await onlinestatus_start_server
    
    asyncio.create_task(aliveChecker())                                                         # Theread für den Alive Checker wird gestartet

    while True: 	                                                                            # (Hauptprogramm) Channel von Redis werden alle abgehört
        message = p.get_message()                                                               # Wenn eine Nachricht reinkommt wird diese verarbeitet
        if message and message['type'] == 'message':
            await handleLogs(message)
        await asyncio.sleep(0.01) 

# Eingehende Nachrichten werden hier verarbeitet
async def handleLogs(message):
    channel = message['channel'].decode('utf-8')                                                # Source Channel
    data = json.loads(message['data'])                                                          # Daten werden Extrahiert
    
    if data['type'] == 'info' or data['type'] == 'success':                                     # Es handelt sich um einen normalen Log 
        logging.info(beautifyLog(channel,data))                                                 # Log wird in eine Datei geschrieben
        await send_logs_to_clients(data)                                                        # Log wird über den Websocket an das Frontend geschickt
    
    elif data['type'] == "error":                                                               # Es handelt sich um einen Fehler
        errorHandling(channel, data)                                                            # Error Handling wird durchgeführt
        await send_logs_to_clients(data)                                                        # Log wird über den Websocket an das Frontend geschickt
    
    elif data['type'] == "online":                                                              # Es handelt sich um einen Online Request
        handleOnlineStatus(channel, data)                                                       # Online Status wird aktualisiert
    
# Logs werden an jedes FrontEnd verteilt
async def send_logs_to_clients(data):
    if connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in connected_clients])

# Online Status wird an jedes FrontEnd verteilt
async def send_online_status(data):
    if onlinestatus_connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in onlinestatus_connected_clients])

# Hier passiert Error Handling
def errorHandling(channel, data):
    logging.error(beautifyLog(channel,data))                                                    # Fehlernachricht wird auf die Platte geschrieben
    heading = f"Komponente {channel.replace('-logs', '')} hat einen fehler"                     # Heading für die Email wird anhand des Channels zusammengebaut (-logs wird entfernt)
    if channel != 'api-logs':                                                                   # Mich nerven die API Fehler, deswegen da keine Emails, sonst gerne
        sendEmail(heading, data["message"])                                                     # Email wird mit Fehler nachricht verschickt
    handleRestart(channel)                                                                      # Neustart wird Initialisiert

# In der Funktion wird an den jeweiligen Channel ein Neustart request verschickt
def handleRestart(channel):
    if channel == 'valentin-logs':
        r.publish('valentin', json.dumps({"request": "restart"}))
    elif channel == 'grafana-logs':
        r.publish('grafana', json.dumps({"request": "restart"}))
    elif channel == 'ada-logs':
        r.publish('ada', json.dumps({"request": "restart"}))
    elif channel == 'sara-logs':
        r.publish('sara', json.dumps({"request": "restart"}))
    elif channel == 'influx-logs':
        r.publish('influx', json.dumps({"request": "restart"}))

# Der Online Status wird hier aktualisiert
def handleOnlineStatus(channel, data):
    global onlinestatus
    if channel == 'valentin-logs':
        onlinestatus['Valentin-Online']['online'] = True
        onlinestatus['Valentin-Online']['timestamp'] = data['timestamp']
    elif channel == 'ada-logs':
        onlinestatus['ADA-Online']['online'] = True
        onlinestatus['ADA-Online']['timestamp'] = data['timestamp']
    elif channel == 'grafana-logs':
        onlinestatus['Grafana-Online']['online'] = True
        onlinestatus['Grafana-Online']['timestamp'] = data['timestamp']
    elif channel == 'sara-logs':
        onlinestatus['SARA-Online']['online'] = True
        onlinestatus['SARA-Online']['timestamp'] = data['timestamp']
    elif channel == 'influx-logs':
        onlinestatus['Database-Online']['online'] = True
        onlinestatus['Database-Online']['timestamp'] = data['timestamp']
    if channel == "api-logs":
        return


# Logs werden etwas lesbarer aufgehübscht
def beautifyLog(channel, data):
    message = f"  {data['timestamp']}   {channel}: {data['message']}"
    return message

# Email wird gesendet
def sendEmail(subject, body):
    senderEmail = 'services@maytastix.de'
    receiver_email = 'aronseidl17@gmail.com'
    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(link, port) as server:
        server.ehlo()
        server.starttls()
        server.login(senderEmail, password)
        server.sendmail(senderEmail, receiver_email, message.as_string())


# Der Thread fragt alle 2 Minuten ob alle Systeme Online sind
async def aliveChecker():
    while True:
        await checkAliveness()                                                                  # Anfrage an alle Komponenten ob sie online sind
        await asyncio.sleep(60)                                                                 # Es wird eine Minute gewarten dass die Systeme Zeit haben zu antworten
        await update_online_status()                                                            # Online Status wird geupdatet
        payload = {"Grafana-Online": onlinestatus['Grafana-Online']['online'],                  # Payload fürs Fronend wird aufbereitet
                   "Database-Online": onlinestatus['Database-Online']['online'],
                   "ADA-Last-Online":onlinestatus['ADA-Online']['timestamp'],
                    "SARA-Last-Online" : onlinestatus['SARA-Online']['timestamp'] }
        await send_online_status(payload)                                                       # Online Status wird an jedes Fronend geschickt
        await asyncio.sleep(60)                                                                 # Es wird wieder eine Minute gewartet


async def update_online_status():
    global onlinestatus
    now = datetime.now()                                                                        # Momentane Zeit wird abgefragt
    time_difference = timedelta(minutes=20)                                                     # 20 Minuten unterschied
    
    for key, value in onlinestatus.items():                                                     # Zeitstempel aller Komponenten wird abgefragt
        timestamp = datetime.strptime(value["timestamp"], "%Y-%m-%d %H:%M:%S")                  
        if now - timestamp > time_difference:                                                   # Wenn der Letzte Wert länger als 20 Minuten her ist, wird online Status aktualisiert
            onlinestatus[key]["online"] = False

async def checkAliveness():                                                                     
    for channel in publisherList:                                                               # Online Request an jede Komponente
        r.publish(channel,json.dumps({"request": "online"}))

asyncio.run(redis_listener())                                                                   # Hauptprogramm wird ausgeführt
