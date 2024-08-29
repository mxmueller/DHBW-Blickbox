#ifndef SERIAL_STUBS_HPP
#define SERIAL_STUBS_HPP

#ifdef unity_testing


// Stubs für die Methoden von Serial
namespace Serial {
    void begin(unsigned long baudrate) {
        // Stub-Implementierung für begin
    }

    void print(const char* str) {
        // Stub-Implementierung für print
    }

    void println(const char* str) {
        // Stub-Implementierung für println
    }

    // Weitere Methoden können hier hinzugefügt werden, wenn nötig
}


#endif  // SERIAL_STUBS_HPP
#endif