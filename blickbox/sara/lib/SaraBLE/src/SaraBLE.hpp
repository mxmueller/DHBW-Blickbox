#ifndef SARABLE_HPP
#define SARABLE_HPP

#include <Arduino.h>
#include <ArduinoBLE.h>
#include <SerialLogger.hpp>



namespace sara_ble{

  class SaraBLE {
    public:
      SaraBLE();
      void begin();
      void loop(uint16_t temperature);
    private:


    BLEService airService; 

    BLECharacteristic temperatureCharacteristic;
  };
}

#endif  // SARABLE_HPP

