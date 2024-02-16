# Sara (Sensor Acquisition and Remote Analysis)

Sensor Appliance Firmware for Blickbox 

# Installation
[Plattform IO Installations Anleitung](https://platformio.org/platformio-ide)
Sara benutzt Plattform IO für Dependancy Mangement, Libraries, Flashing und Compilation.



# Nutzung
Sara ist dazu da die Sensoren der Wetterstation auszulesen. Dafür werden Kommandos verwendet, 
die über die Serielle Schnittstelle übertragen werden.
Um eine Serielle Verbindung herzustellen kann minicom, der Arduino Serielle Monitor oder der serielle Monitor von Platform IO
verwendet werden. Auf der getesteten Maschiene wird der Arduino über ``/dev/ttyACM0`` addressiert.
Das Kommunikation wird über **115200 Baud** geführt
Zur Aggregation der Daten soll auf Ada (Automatic Digital Aggregator) zurückgegriffen werden.
Dieses Programm sammelt die Daten in spezifizierten Zeitabständen, legt diese als csv Datei ab und kann diese dann in
die Cloud Umgebung übertragen.

## Minicom
```bash
minicom -D /dev/ttyACM0 -b 115200
```

# Übertragung
Komando müssen über ein CR LF angänsel übermittelt werden
Das würde dann so aussehen:
```c
serial.write("t\r\n");
```

Sara übermittelt dann die Daten in dem Muster:
Computer --> "t\r\n"
"t:20.45\r\n"