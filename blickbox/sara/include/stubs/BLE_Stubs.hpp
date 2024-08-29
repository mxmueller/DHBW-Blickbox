// stubs/ArduinoBLEStubs.hpp

#ifndef ARDUINOBLESTUBS_HPP
#define ARDUINOBLESTUBS_HPP

#include <string>
#include <map>
#include <functional>
#include <types/Numbers.h>

// Stub for BLECharacteristic
class BLECharacteristic {
public:
    BLECharacteristic(const char* uuid, unsigned char properties, int size = 20, bool fixedLength = false) {}
    void writeValue(uint16_t value) {}
    void writeValue(const std::string& value) {}
    std::string value() const { return ""; }
};

// Stub for BLEService
class BLEService {
public:
    BLEService(const char* uuid) {}
    bool begin() { return true; }
    void addCharacteristic(BLECharacteristic& characteristic) {}
};

// Stub for BLEDevice
class BLEDevice {
public:
    std::string address() const { return "00:00:00:00:00:00"; }
};

// BLE Event Types
enum BLEEvent {
    BLEConnected,
    BLEDisconnected
};

// Stubs for BLE functions
namespace BLE {
    std::map<BLEEvent, std::function<void(BLEDevice)>> eventHandlers;

    bool begin() { return true; }
    void setEventHandler(BLEEvent event, std::function<void(BLEDevice)> handler) {
        eventHandlers[event] = handler;
    }
    BLEDevice central() { return BLEDevice(); }
    void advertise() {}
    void stopAdvertise() {}
    void setLocalName(const char* name) {}
    void setAdvertisedService(BLEService& service) {}
    void addService(BLEService& service) {}

    // Simulate BLE Events (for testing)
    void simulateConnect() {
        if (eventHandlers[BLEConnected]) {
            eventHandlers[BLEConnected](BLEDevice());
        }
    }

    void simulateDisconnect() {
        if (eventHandlers[BLEDisconnected]) {
            eventHandlers[BLEDisconnected](BLEDevice());
        }
    }
}

#endif // ARDUINOBLESTUBS_HPP
