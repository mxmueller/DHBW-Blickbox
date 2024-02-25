#ifndef SARABLE_HPP
#define SARABLE_HPP

#include <Arduino.h>
#include <ArduinoBLE.h>
#include <SerialLogger.hpp>
#include <sara_data.hpp>



namespace sara_ble{

  enum ble_state{
    NONE,
    DISCONNECTED,
    CONNECTED
  };

  String ble_state_to_String(ble_state state);

  class SaraBLE {
    public:
      SaraBLE();
      void begin();
      ble_state get_connection_state();
      String get_connected_device();
      void print_bluetooth_state();
      void loop();
    private:

      void update_connection_state(BLEDevice *ble_device);

      // Verbinungs infos
      ble_state connection_state = NONE;
      ble_state last_connection_state = NONE;
      String connected_device;

      // BLE Services
      BLEService airService; 

      BLECharacteristic temperatureCharacteristic;
      BLECharacteristic humidityCharacteristic;

      BLEService weatherStationService; 

      BLECharacteristic rainfallCharacteristic;
      BLECharacteristic winddirectionCharacteristic;
      BLECharacteristic windspeedCharacteristic;
  };
}

#endif  // SARABLE_HPP

