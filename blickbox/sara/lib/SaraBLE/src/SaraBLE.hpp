#ifndef SARABLE_HPP
#define SARABLE_HPP

#include <Arduino.h>
#include <ArduinoBLE.h>
#include <SerialLogger.hpp>
#include <FireTimer.h>
#include <sara_definitions.hpp>



namespace sara_ble{

  enum ble_state{
    NONE,
    CONNECTED,
    DISCONNECTED
  };


  class SaraBLE {
    public:
      SaraBLE();
      void begin();
      void loop();
    private:

    FireTimer sensor_poll_timer;
    ble_state state = NONE; 

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

