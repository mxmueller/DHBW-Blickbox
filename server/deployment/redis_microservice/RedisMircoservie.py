import redis
import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import websockets
import os


link = os.getenv("EMAIL_SMTP_SERVER")
port = os.getenv("EMAIL_SMTP_PORT")
password = os.getenv("EMAIL_SMTP_PASSWORD")


r = redis.Redis(host='redis', port=6379, db=0)
p = r.pubsub()
logging.getLogger('websockets').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.basicConfig(filename='./logdaten/system_logs.log', level=logging.INFO)

p.subscribe(["api-logs", "valentin-logs", "grafana-logs", "ada-logs", "sara-logs"])

publisherList = ["backend", "grafana", "ada", "sara", "valentin"]


connected_clients = []


async def websocket_server(websocket, path):
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            pass  
    finally:

        connected_clients.remove(websocket)

async def redis_listener():

    start_server = websockets.serve(websocket_server, "0.0.0.0", 5001)
    

    await start_server
    
   
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
    elif data['type'] == "error":
        errorHandling(channel, data)

    await send_logs_to_clients(data)

async def send_logs_to_clients(data):
    if connected_clients:
        message = json.dumps(data)
        await asyncio.gather(*[client.send(message) for client in connected_clients])

def errorHandling(channel, data):
    logging.error(beautifyLog(channel,data))
    heading = f"Komponente {channel.replace('-logs', '')} hat einen fehler"
    sendEmail(heading, data["message"])
    if channel == "api-logs":
        return
    for item in publisherList:
        r.publish(item, "Restart Bitch")

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

asyncio.run(redis_listener())
