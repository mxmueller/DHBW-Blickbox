## SARA (Datenerfassung)
FEHLT -> May

## SOPS
FEHLT -> May

## Grafana (Datenerfassung)
FEHLT -> Aron

## Backend-Service
FEHLT -> ARON

## Monitoring-Service
FEHLT -> ARON

## Backend-Service
FEHLT -> May

## NGINX
FEHLT -> May

## Jenknins Pipline
Diese Teil beschreibt die Einrichtung, Verwendung und Details der Jenkins-Pipeline für das Blickbox-Projekt.
### Einrichtung der Jenkins-Pipeline

1. Öffnen Sie Jenkins unter http://maytastix.de:3005/jenkins/
2. Erstellen Sie ein neues Pipeline-Projekt:
   - Klicken Sie auf "Neue Item" im Jenkins-Dashboard
   - Geben Sie einen Namen für Ihr Projekt ein
   - Wählen Sie "Pipeline" als Projekttyp
   - Klicken Sie auf "OK"
3. Konfigurieren Sie die Pipeline:
   - Scrollen Sie zum Abschnitt "Pipeline"
   - Wählen Sie "Pipeline script from SCM" als Definition
   - Wählen Sie "Git" als SCM
   - Geben Sie die URL Ihres Git-Repositories ein
   - Stellen Sie sicher, dass der Branch "production" ausgewählt ist
   - Setzen Sie "Jenkinsfile" als Script-Pfad
4. Speichern Sie die Konfiguration.

### Verwendung der Pipeline

Die Pipeline wird automatisch ausgeführt, wenn Änderungen im "production" Branch erkannt werden. Sie können sie auch manuell starten:
1. Navigieren Sie zu Ihrem Pipeline-Projekt in Jenkins
2. Klicken Sie auf "Build Now"

### Pipeline-Schritte im Detail

Die Pipeline durchläuft folgende Hauptphasen:

| Schritt | Beschreibung |
|---------|--------------|
| Git Checkout | Lädt den aktuellen Code aus dem Git-Repository |
| Git GitLeaks Scan | Führt einen GitLeaks-Scan durch, um sensible Daten im Code zu identifizieren |
| SARA Setup, Tests und Linting | Richtet die Build-Umgebung für SARA ein, führt Unit-Tests und Code-Linting durch |
| ADA Setup, Build, Test und Linting | Richtet die Rust-Umgebung ein, baut das ADA-Projekt, führt Tests und Sicherheits-Audits durch |
| Backend Setup, Tests und Sicherheit | Richtet die Python-Umgebung ein, führt API-Tests, Microservice-Tests und Sicherheits-Scans durch |
| Valentin Build, Tests und Sicherheit | Baut das VALENTIN-Projekt, führt Tests und Sicherheits-Checks durch |
| Docker Dockerfile Analyse | Analysiert alle Dockerfiles im Projekt mit Hadolint |
| Deployment Copy to Deploy Directory | Kopiert das Projekt in das Deployment-Verzeichnis und entschlüsselt Zugangsdaten |
| Deployment Launch | Startet die Docker-Container für die Produktion |

### Hinzufügen neuer Schritte zur Pipeline

Um neue Schritte zur Pipeline hinzuzufügen:

1. Öffnen Sie die `Jenkinsfile` im Root-Verzeichnis des "production" Branches.

2. Fügen Sie einen neuen `stage` Block hinzu. Beispiel:

   ```groovy
   stage('Neuer Schritt') {
       steps {
           // Ihre Befehle hier
           sh 'echo "Dies ist ein neuer Schritt"'
       }
   }
   ```

3. Platzieren Sie den neuen `stage` Block an der gewünschten Stelle in der Pipeline.

4. Committen und pushen Sie Ihre Änderungen zum "production" Branch.

5. Jenkins wird die aktualisierte Pipeline automatisch verwenden.

### Tipps für die Erweiterung der Pipeline

- Gruppieren Sie zusammengehörige Schritte in einem `stage`.
- Verwenden Sie aussagekräftige Namen für Ihre Stages.
- Nutzen Sie Umgebungsvariablen für wiederverwendbare Werte.
- Fügen Sie Post-Actions hinzu, um auf Erfolg oder Fehler zu reagieren.
- Nutzen Sie Parallel-Schritte für unabhängige Aufgaben, um die Ausführungszeit zu reduzieren.
- Denken Sie daran, neue Tools oder Abhängigkeiten im Jenkins-Umfeld zu installieren, wenn Sie sie in der Pipeline verwenden möchten.

### Fehlerbehebung

- Überprüfen Sie die Konsolenausgabe in Jenkins für detaillierte Fehlerinformationen.
- Stellen Sie sicher, dass alle erforderlichen Tools und Abhängigkeiten auf dem Jenkins-Server installiert sind.
- Überprüfen Sie die Berechtigungen, wenn Zugriffsprobleme auftreten.
- Bei Problemen mit spezifischen Stages, isolieren Sie den Schritt und führen Sie ihn manuell aus, um das Problem einzugrenzen.
- Überprüfen Sie die Versionen der verwendeten Tools und aktualisieren Sie sie gegebenenfalls.

Bei Fragen oder Problemen wenden Sie sich bitte an das DevOps-Team.

## Valentin Dashboard
Dieses Projekt wurde mit [Create React App](https://github.com/facebook/create-react-app) erstellt.

### Verfügbare Skripte

Im Projektverzeichnis können Sie folgende Befehle ausführen:
#### `npm install`
#### `npm start`

Startet die App im Entwicklungsmodus.\
Öffnen Sie [http://localhost:3000](http://localhost:3000), um sie im Browser anzuzeigen.

Die Seite wird automatisch neu geladen, wenn Sie Änderungen vornehmen.\
#### `npm run build`

Erstellt die App für die Produktion im `build`-Ordner.\
Es bündelt React korrekt im Produktionsmodus und optimiert den Build für die beste Performance.\
Der Build wird minifiziert und die Dateinamen enthalten Hashes.

## ADA (Datenvermittlung)

### Rust Toolchain installieren oder updaten
Hier sind die Schritte zur Weiterentwicklung mit Rust aufgeführt.

Zuerst muss Rustup heruntergeladen werden, um Rust zu installieren.
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Um die neuste Version von Rust zu verwenden, updatet folgender Befehl die Rust-Version.
```bash
rustup update
```

Jetzt kann Rust im Projekt verwenden werden.
```bash
cd blickbox/ada
```
### Funktionsfähigkeit von ADA
Um ADA einzusetzen, muss das Gerät, auf dem ADA läuft, Bluetooth- und WLAN-fähig sein.

### Weitere Informationen
- [Rust-lang](https://www.rust-lang.org/)

## MkDocs mit GitHub Pages

Dieses Repository enthält die Dokumentation für DHBW-Blickbox, erstellt mit MkDocs und gehostet auf GitHub Pages.

Folgen Sie diesen Schritten, um das Projekt einzurichten und die Dokumentation zu deployen:

### MkDocs-Projekt Abhänigkeit

```bash
# MkDocs installieren
pip install mkdocs
pip install mkdocs-material

# In das Projektverzeichnis wechseln
cd docs/mkdocs/
```

### Aktualisierungen vornehmen
- Nehmen Sie Änderungen an Ihren Markdown-Dateien vor
- Committen und pushen Sie die Änderungen:

```bash
git add .
# Richter Branche
git commit -m "Update documentation" # Richter Branche
git push
```

- Deployen Sie die aktualisierten Seiten:
```bash
mkdocs gh-deploy
```
Die Änderung erscheint nach einigen Minuten unter [https://mxmueller.github.io/DHBW-Blickbox](https://mxmueller.github.io/DHBW-Blickbox) in Ihrem Browser.

### Lokale Entwicklung
Um die Dokumentation lokal zu testen, führen Sie folgenden Befehl aus:
```bash
mkdocs serve
```

Öffnen Sie dann [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in Ihrem Browser.

### Weitere Informationen

- [MkDocs Dokumentation](https://www.mkdocs.org/)
- [GitHub Pages Dokumentation](https://docs.github.com/en/pages)

## C4 Diagramme

### Mermaid für Diagramme
Nach dem Vergleich verschiedener Technologien fällt die Wahl auf den Mermaid Live Editor.
Dieser kann wie folgt aufgerufen werden:
[https://mermaid.live/](https://mermaid.live/)

#### Aufbau von Mermaid
Die Dokumentation von mermaid zu C4 findet sich unter:
[https://mermaid.js.org/syntax/c4.html](https://mermaid.js.org/syntax/c4.html)

Die Syntax von PlantUML kann verwendet werden: [https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md](https://github.com/plantuml-stdlib/C4-PlantUML/blob/master/README.md)

Basiscode Beispiel eines C4 Diagramms:

    C4Context
      title System Context diagram for Internet Banking System
      Enterprise_Boundary(b0, "BankBoundary0") {
        Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
        Person(customerB, "Banking Customer B")
        Person_Ext(customerC, "Banking Customer C", "desc")

        Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

        System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

        Enterprise_Boundary(b1, "BankBoundary") {

          SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

          System_Boundary(b2, "BankBoundary2") {
            System(SystemA, "Banking System A")
            System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
          }

          System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
          SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

          Boundary(b3, "BankBoundary3", "boundary") {
            SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
            SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
          }
        }
      }

      BiRel(customerA, SystemAA, "Uses")
      BiRel(SystemAA, SystemE, "Uses")
      Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
      Rel(SystemC, customerA, "Sends e-mails to")

      UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
      UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
      UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")


[Zurück zur Hauptseite](../index.md)
