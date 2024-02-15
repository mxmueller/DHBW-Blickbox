# Externer Server Block

Dieser Teil beinhaltet die serverseitigen Anwendungen der DHBW-Blickbox. 
Sie bestehen aus:
- Reverse Proxy
- InfluxDB
- Grafana-Server
- Python API

Jede dieser Anwendungen laufen in einem Docker-Container.

# Start UP
Um den Service zu starten muss folgender Command eingegeben werden:

```bash
docker-compose -up
```

# Erreichbarkeit
Wie aus der Docker-Compose Datei zu entnehmen sind die Anwendungen unter folgenden Ports erreichbar:
- Reverse-Proxy:  Port 443
- InfluxDB:       Port 8086
- Grafana:        Port 3000
- Python API:     Port 5000


