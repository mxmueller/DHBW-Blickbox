# Unittests in Rust

Die Unittests testen die Logik von ADA, die die eingehenden Sensordaten verarbeitet.
Um nur die Tests auszuführen, führt man aus dem ada-directory `cargo test` aus.
Dadurch werden die _dev-dependencies_ aus der Cargo.toml genutzt.
Da nur in den Tests das Crate _mockito_ genutzt wird, wird es nur in Tests kompiliert.

Ist die Hardware nicht angeschlossen, kann der Befehl `cargo run --features "mock"` ausgeführt werden.
Dabei werden Mock-Daten verwendet und diese an die API gesendet.
