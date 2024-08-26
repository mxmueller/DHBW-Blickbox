// ArduinoStubs.hpp


#ifndef ARDUINO_STUBS_HPP
#define ARDUINO_STUBS_HPP

#include <cstdint>

// Stub für pinMode
inline void pinMode(uint8_t pin, uint8_t mode) {
    // Keine Aktion
}

// Stub für analogRead
inline int analogRead(uint8_t pin) {
    return 0;  // Dummy-Wert, kann angepasst werden
}

inline void digitalWrite(uint8_t pin, bool status) {
    
}

// Stub für delay
inline void delay(uint32_t ms) {
    // Keine Aktion
}

inline uint32_t millis() {
    return 1;
}



// Weitere benötigte Arduino-Funktionen hier stubs bereitstellen

#endif // ARDUINO_STUBS_HPP
