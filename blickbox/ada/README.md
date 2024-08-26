
# Unittests in Rust

Die Unittests testen die Logik von ADA, die die eingehenden Sensordaten verarbeitet.

Unittests befinden sich in den Modul-Dateien, in denen sich die Logik befindet und sind mit `#[cfg(test)]` gekennzeichnet.

Um alle Tests auszuführen, führt man aus dem ada-directory `cargo test` aus.
