# Installieren auf Raspberry Pi
Führe dazu das ``install.sh`` script aus. Dieses compiled den aktuellen Stand und kopiert den aktuellen Stand in ``usr/local/ada``
Systemd wird die Datei von diesem Punkt das Program automatisch starten.

Damit alles auf dem Raspberry läuft müssen verschiedene Libraries installiert werden
```bash
sudo apt install libssl-dev libudev-dev libusb-1.0-0-dev libftdi1-dev pkg-config libdbus-1-dev libudev-sys  
```

# Compiling
Führe das Program mit ``cargo run`` aus oder baue es mit ``cargo build```
