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


onlinestatus = {
                "Valentin-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "Grafana-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "Database-Online" : {"online" : False, "timestamp" : "1970-1-1 00:00:00"}, 
                "ADA-Online": {"online" : False, "timestamp" : "1970-1-1 00:00:00"},
                "SARA-Online": {"online" : False, "timestamp" : "1970-1-1 00:00:00"}
                }


link = os.getenv("EMAIL_SMTP_SERVER")
port = os.getenv("EMAIL_SMTP_PORT")
password = os.getenv("EMAIL_SMTP_PASSWORD")



r = redis.Redis(host='redis', port=6379, db=0)
p = r.pubsub()
logging.getLogger('websockets').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.basicConfig(filename='./logdaten/system_logs.log', level=logging.INFO)

p.subscribe(["api-logs", "valentin-logs", "grafana-logs", "ada-logs", "sara-logs", "influx-logs"])

publisherList = ["backend","valentin",  "ada", "sara", "grafana", "influx"]


connected_clients = []
onlinestatus_connected_clients = []

async def websocket_server(websocket, path):
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            pass  
    finally:

        connected_clients.remove(websocket)


async def onlinestatus_server(websocket, path):
    onlinestatus_connected_clients.append(websocket)
    try:
        async for message in websocket:
            pass  
    finally:
        onlinestatus_connected_clients.remove(websocket)

async def redis_listener():
    start_server = websockets.serve(websocket_server, "0.0.0.0", 5001)
    await start_server
    onlinestatus_start_server = websockets.serve(onlinestatus_server, "0.0.0.0", 5002)
    await onlinestatus_start_server
    
    asyncio.create_task(aliveChecker())

    while True:
        message = p.get_message()
        if message and message['type'] == 'message':
            await handleLogs(message)
        await asyncio.sleep(0.01) 

async def handleLogs(message):
    channel = message['channel'].decode('utf-8')
    data = json.loads(message['data'])
    if data['type'] == 'info' or data['type'] == 'success':
        logging.info(beautifyLog(channel,data))
        await send_logs_to_clients(data)
    elif data['type'] == "error":
        errorHandling(channel, data)
        await send_logs_to_clients(data)
    elif data['type'] == "online":
        handleOnlineStatus(channel, data)
    

async def send_logs_to_clients(data):
    if connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def send_online_status(data):
    if onlinestatus_connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in onlinestatus_connected_clients])

def errorHandling(channel, data):
    logging.error(beautifyLog(channel,data))
    heading = f"Komponente {channel.replace('-logs', '')} hat einen fehler"
    if channel != 'api-logs':
        sendEmail(heading, data["message"])

    handleRestart(channel)

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
    for item in publisherList:
        r.publish(item, "Restart")


def beautifyLog(channel, data):
    message = f"  {data['timestamp']}   {channel}: {data['message']}"
    return message

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


async def aliveChecker():
    while True:
        await checkAliveness()
        await asyncio.sleep(60)
        await update_online_status()
        payload = {"Grafana-Online": onlinestatus['Grafana-Online']['online'],
                   "Database-Online": onlinestatus['Database-Online']['online'],
                   "ADA-Last-Online":onlinestatus['ADA-Online']['timestamp'],
                    "SARA-Last-Online" : onlinestatus['SARA-Online']['timestamp'] }
        await send_online_status(payload)
        await asyncio.sleep(60)

async def update_online_status():
    global onlinestatus
    now = datetime.now()
    
    time_difference = timedelta(minutes=20)
    
    for key, value in onlinestatus.items():
        timestamp = datetime.strptime(value["timestamp"], "%Y-%m-%d %H:%M:%S")
        
        if now - timestamp > time_difference:
            onlinestatus[key]["online"] = False

async def checkAliveness():
    for channel in publisherList:
        r.publish(channel,json.dumps({"request": "online"}))

asyncio.run(redis_listener())
