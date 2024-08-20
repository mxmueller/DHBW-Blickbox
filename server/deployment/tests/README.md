
# Test Suite für die API

## Unit Tests mit Pytest

Diese Unittests Testen die Funktionalität der API. Hauptsächlich wird getestet wie die API mit falschen Eingabeparametern umgeht. Hierfür wird jede Route durchgetestet.

### Installation

  

    pip install -r reqirements.txt

  

### Nutzung

  

    pytest API-Tests.py -v --junitxml=report.xml <optionale Parameter>

-v steht für verbose um mehr Informationen anzeigen zu lassen, --junitxml=report.xml erstellt einen Test-Report

Zu den Optionalen Parametern gehören:

  

-  **--noPing** | Tests werden ohne die Ping-Logik ausgeführt

-  **--noTemp** | Tests werden ohne die Temperatur-Route ausgeführt

-  **--noHumid** | Tests werden ohne die Luftfeuchtigkeit-Route ausgeführt

-  **--noWindDir** | Tests werden ohne die Windrichtungs-Route ausgeführt

-  **--noWindSpeed** | Tests werden ohne die Windgeschwindigkeits-Route ausgeführt

-  **--noRain** | Tests werden ohne die Niederschlag-Route ausgeführt

-  **--noBatteryC** | Tests werden ohne die Batterieladung-Route ausgeführt
-  **--noBatteryV** | Tests werden ohne die Batteriespannung-Route ausgeführt
