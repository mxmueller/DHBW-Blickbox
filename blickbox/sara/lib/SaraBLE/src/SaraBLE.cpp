#include <SaraBLE.hpp>

namespace sara_ble{
    using namespace serial_logger;

    SaraBLE::SaraBLE() : airService("1101"), temperatureCharacteristic("2101", BLERead | BLENotify, 16) {
    }

    void SaraBLE::begin(){
        
        if (!BLE.begin()) {
            log(F("r:ble_failed:Starting BLE failed!"), ERROR);
            while (1);
        }
        BLE.setLocalName("SARA Weather Station");
        BLE.setAdvertisedService(airService);
        airService.addCharacteristic(temperatureCharacteristic);
        BLE.addService(airService);

        BLE.advertise();
    }

    void SaraBLE::loop(uint16_t temperature){
       BLEDevice central = BLE.central();

        if (central) 
        {
        Serial.print("Connected to central: ");
        Serial.println(central.address());
        digitalWrite(LED_BUILTIN, HIGH);

        while (central.connected()) {

                Serial.print("Temperatur is now: ");
                Serial.println(temperature);
                temperatureCharacteristic.writeValue(temperature);
                delay(200);

        }
        }
        digitalWrite(LED_BUILTIN, LOW);
        Serial.print("Disconnected from central: ");
        Serial.println(central.address());
    }
}