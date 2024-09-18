## SARA (Datenerfassung)
FEHLT -> May

## Backend-Service & Monitoring-Service
### Vorbereiteung
Im Verzeichnis ```/server/deployment/tests ``` führen Sie folgenden Befehl aus:
```bash
 pip install -r requirements.txt
```

### Tests ausführen
Im Verzeichnis ```/server/deployment/tests ``` führen Sie folgenden Befehl aus:
```bash
pytest API-Tests.py -v --junitxml=report.xml <optionale Parameter>
```

-v steht für verbose um mehr Informationen anzeigen zu lassen <br>
--junitxml=report.xml erstellt einen Test-Report

Zu den Optionalen Parametern gehören:


-  **--noPing** | Tests werden ohne die Ping-Logik ausgeführt

-  **--noTemp** | Tests werden ohne die Temperatur-Route ausgeführt

-  **--noHumid** | Tests werden ohne die Luftfeuchtigkeit-Route ausgeführt

-  **--noWindDir** | Tests werden ohne die Windrichtungs-Route ausgeführt

-  **--noWindSpeed** | Tests werden ohne die Windgeschwindigkeits-Route ausgeführt

-  **--noRain** | Tests werden ohne die Niederschlag-Route ausgeführt

-  **--noBatteryC** | Tests werden ohne die Batterieladung-Route ausgeführt
-  **--noBatteryV** | Tests werden ohne die Batteriespannung-Route ausgeführt

Bei der Test Ausführung können entweder die Production Routen, oder die lokalen Developer Routen getestet werden.
Um lokal zu testen müssen Sie Docker installieren und in einer ``` .env ```-Datei folgende Umgebungsvariable setzen: 
``` API_USE_DEV_CONTAINER = true```

### Tests schreiben
Um Tests zu schreiben kann die ```API-Tests.py``` erweitert werden. Funktionen die im Test-Prozess beachtet werden sollen müssen mit ```test_``` beginnen.
## Valentin Dashboard
Dieses Projekt wurde mit [Create React App](https://github.com/facebook/create-react-app) erstellt. \
Im Projektverzeichnis können Sie folgende Befehle ausführen:
```bash
 npm test
```
### Tests ausführen

Dieses Projekt verwendet Jest für Tests. So führen Sie die Tests aus:

1. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind, indem Sie `npm install` ausführen
2. Führen Sie `npm test` aus, um den Testrunner im Watch-Modus zu starten
3. Drücken Sie `a`, um alle Tests auszuführen

### Tests schreiben

- Tests befinden sich im `__tests__`-Verzeichnis oder neben den Komponenten mit der Erweiterung `.test.js` oder `.spec.js`
- Verwenden Sie `describe`, um zusammengehörige Tests zu gruppieren
- Verwenden Sie `it` oder `test`, um einzelne Testfälle zu definieren
- Verwenden Sie `expect` für Behauptungen

Beispiel:

```javascript
import { render, screen } from '@testing-library/react';
import App from './App';

test('rendert den "Learn React" Link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
```

### Mehr erfahren

Sie können mehr in der [Create React App Dokumentation](https://facebook.github.io/create-react-app/docs/getting-started) erfahren.

Um React zu lernen, schauen Sie sich die [React-Dokumentation](https://reactjs.org/) an.

## ADA (Datenvermittlung)

### Programm im Dev-Modus ausführen

Sollte die Wetterstation nicht angebunden sein, kann man generierte Mock-Sensordaten verwenden, um unabhängig von der Wetterstation ADA auszuführen.
Der Code wird dabei mit folgender Konfiguration gestartet:

```bash 
cargo run --features "mock"
```

Dabei werden Mock-Daten verwendet und diese an die API gesendet.


### Unittests in Rust

Die Unittests testen die Logik von ADA, die die eingehenden Sensordaten verarbeitet.
Unittests befinden sich in dem Modul blickbox/ada/src/tests.
Um alle Tests auszuführen, führt man folgenden Befehl aus dem ada-Ordner aus:

``` bash
 cargo test
```

Beim Testen werden die _dev-dependencies_ aus der Cargo.toml genutzt.
Da nur in den Tests das Crate _mockito_ genutzt wird, wird es nur in Tests kompiliert.