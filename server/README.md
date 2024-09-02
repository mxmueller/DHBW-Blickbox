# Deployment
1. Decrypte die Secrets um mit dem Deploment fortzufahren oder lege deine costum env Datei an.
2. Das Encrypting läuft mit dem SOPS Container lege dazu die valide key.txt in den secrets Ordner und führe ``docker compose up sops`` aus
3. Führe anschließend ``docker compose up -d`` aus
4. Falls das dein erstes Deployment ist gehe auf deine Domain und richte den Reverse Proxy ein
Diese erreichst du über ``domain.de:81``
5. Trage die Service als Proxy Host ein. 
Deine Subdomain kannst du selber wählen in unserem Setup nutzen wir
    - blickbox.maytastix.de
       - http://valentin:80
    - dhbwapi.maytastix.de
      - http://server-python_app-1:5000
    - dhbwgrafana.maytastix.de
      - https://grafana-server:3000
    - npm.maytastix.de
       - http://server-reverse-proxy-1:81
6. Beachte, dass du eventuell eine Weiterleitung in deinen Subdomain Einstellung deines Hosters treffen musst.
Eventuell muss ein A und AAAA Record mit der IP Adresse deines Servers gesetzt werden.

# Ausführen

Mit Build:
``docker compose up --build``

Einzelne Container starten:
```bash
sudo docker compose start python_app  
sudo docker compose start valentin  
sudo docker compose start influxdb  
sudo docker compose start grafana  
sudo docker compose start reverse-proxy
```

Einzelne Container stoppen:
```bash
sudo docker compose stop python_app  
sudo docker compose stop valentin  
sudo docker compose stop influxdb  
sudo docker compose stop grafana  
sudo docker compose stop reverse-proxy
```

Image Cache löschen wenn sich was gändert hat:
```bash
sudo docker system prune
```

Einzelne Container starten und bauen:
```bash
docker-compose build valentin
docker-compose up -d valentin
docker-compose restart valentin
```
