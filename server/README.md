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

# Development Journey

## Ändern des Docker Deployments

Schreibe deine Änderungen, die für die Developement Umgebung gedacht sind in 
``compose.override.yaml``. Diese Datei wird mit docker-compose.yaml  bei ``docker compose up`` gemergt.

``docker-compose.yaml`` dient als Basisdatei und sollte eher nicht geändert werden, da sich das auf die prod Umgebung auswirkt. Änderungen die für Prod als auch Dev gedacht sind können hier gemacht werden. 

Schließt sich prod oder dev aus müssen die Änderungen entweder in ``compose.override.yaml`` (für dev) oder
in ``compose.prod.yaml`` (für prod) gemacht werden.

## Credentials

Für Prod und Dev werden andere Keys verwendet. Alle Entwickler*innen sollten einen Schlüssel für die Dev Credentials haben. Um neue Secrets hinzuzufügen wird ![sops](https://github.com/getsops/sops) auf dem Entwicklungs-PC benötigt.  

Um die Datei zu bearbeiten muss folgende Umgebungsvariable gesetzt werden.
Diese zeigt auf den Schlüssel, der für die Verschlüsselung der secret Datei verwendet wurde.

```bash
SOPS_AGE_KEY_FILE: /secrets/key.txt
```

Mit ``sops edit secrets.dev.enc.env`` kann die Datei bearbeitet werden.
Nach dem Speichern und schließen der Datei wird diese wieder verschlüsselt.

Das Docker Deployment ersetzt die entschlüsselte Datei nach jedem Start, sodass Änderungen in dieser nicht übernommen werden.

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

# Deployment auf Prod ohne nginx proxy manager

1. Erstelle in /srv und /opt einen Ordner
  - Das Deployment ``compose.prod.yml`` nutzt den Ordner /srv/blickbox für die Anwendungsdaten (volumes)
  - Um das Prod Deployment zu starten führe folgendes Kommando aus
  ``docker compose -f compose.prod.yaml up``
2. In /opt wird das Repository geladen
3. In /srv werden die Anwendungsdaten, die bei der Ausführung entstehen gespeichert
4. Die Ports der Anwendungen werden auf localhost weitergeleitet:
  * Port 3000 -> Grafana
  * Port 3001 -> Valentin
  * Port 3002 -> API
5. Für die Service sind folgende Routen vorgesehen
  * https://blickbox.maytastix.de -> Valentin
  * https://blickbox.maytastix.de/api -> API
  * https://blickbox.maytastix.de/grafana -> Grafana
6. Konfigurieren des Reverse Proxies
Das Deployment nutzt einen auf dem Server laufenden Nginx Reverse Proxy welcher mit der Datei blickbox.maytastix.de konfiguriert wurde
* Erstelle die Datei blickbox.maytastix.de mit folgenden Inhalt
```json
server {
        listen 80;
        listen [::]:80;
        root /var/www/blickbox.maytastix.de;
        index index.html;
        server_name blickbox.maytastix.de;
}
```
* Erstelle einen Symbolic Link um die Konfiguration nginx bekannt zu machen
``ln -s /etc/nginx/sites-available/blickbox.maytastix.de /etc/nginx/sites-enabled/``
* Rufe certbot auf und erstelle ein Zertifikat für blickbox.maytastix.de
* Füge anschließend folgenden Inhalt unter die Zeilen ein.

```
root /var/www/blickbox.maytastix.de;
index index.html;
server_name blickbox.maytastix.de;
```

```json
   location / {
        proxy_pass http://localhost:3001/; 
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        client_max_body_size 0;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

        access_log /var/log/nginx/valentin.access.log;
        error_log /var/log/nginx/valentin.error.log;
    }

    location /api/ {
            proxy_pass http://localhost:3002/; 
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            client_max_body_size 0;
            add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

            access_log /var/log/nginx/api.access.log;
            error_log /var/log/nginx/api.error.log;
    }

    location /grafana/ {
            proxy_pass http://localhost:3000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            client_max_body_size 0;
            add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

            access_log /var/log/nginx/graphana.access.log;
            error_log /var/log/nginx/graphana.error.log;
    }
```

* Vergleich die Datei /server/prod/blickbox.maytastix.de mit deiner Konfiguration
* Reloade nginx ``systemctl reload nginx``
8. Deine Services solltem über folgende Links erreichbar sein
  * https://blickbox.maytastix.de -> Valentin
  * https://blickbox.maytastix.de/api -> API
  * https://blickbox.maytastix.de/grafana -> Grafana

## Troubleshooting

Auf dem verwendeten Server wurde für /srv/blickbox/graphana_data keine schreibberechtigung gesetzt um das zu fixen muss für die Gruppe das w-flag
gesetzt werden.

```bash
chmod g+w grafana_data/
```