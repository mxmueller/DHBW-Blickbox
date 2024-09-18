# Programm im Dev-Modus ausführen

Sollte die Wetterstation nicht angebunden sein, kann man generierte Mock-Sensordaten verwenden, um unabhängig von der Wetterstation ADA auszuführen.
Der Code wird dabei mit folgender Konfiguration gestartet:

```bash 
cargo run --features "mock"
```
Dabei werden Mock-Daten verwendet und diese an die API gesendet.

# Unittests in Rust

Die Unittests testen die Logik von ADA, die die eingehenden Sensordaten verarbeitet.
Unittests befinden sich in dem Modul blickbox/ada/src/tests.
Um alle Tests auszuführen, führt man folgenden Befehl aus dem ada-Ordner aus:

``` bash
 cargo test
```

Beim Testen werden die _dev-dependencies_ aus der Cargo.toml genutzt.
Da nur in den Tests das Crate _mockito_ genutzt wird, wird es nur in Tests kompiliert.