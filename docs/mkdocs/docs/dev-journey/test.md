## SARA (Datenerfassung)
FEHLT -> May

## Backend-Service & Monitoring-Service
FEHLT -> ARON

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

### Unittests in Rust

Die Unittests testen die Logik von ADA, die die eingehenden Sensordaten verarbeitet.
Unittests befinden sich in dem Modul blickbox/ada/src/tests.
Um alle Tests auszuführen, führt man folgenden Befehl aus dem ada-Ordner aus:

``` bash
 cargo test
```
