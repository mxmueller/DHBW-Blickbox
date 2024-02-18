# Deployment
1. Führe ``docker compose up -d`` aus
2. Falls das dein erstes Deployment ist gehe auf deine Domain und richte den Reverse Proxy ein
Diese erreichst du über ``domain.de:81``
3. Trage die Service als Proxy Host ein. 
Deine Subdomain kannst du selber wählen in unserem Setup nutzen wir
    - blickbox.maytastix.de
       - http://valentin:80
    - dhbwapi.maytastix.de
      - http://server-python_app-1:5000
    - dhbwgrafana.maytastix.de
      - https://grafana-server:3000
    - npm.maytastix.de
       - http://server-reverse-proxy-1:81
4. Beachte, dass du eventuell eine Weiterleitung in deinen Subdomain Einstellung deines Hosters treffen musst.
Eventuell muss ein A und AAAA Record mit der IP Adresse deines Servers gesetzt werden.
