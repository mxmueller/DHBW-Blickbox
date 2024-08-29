#ifndef SARABLE_HPP
#define SARABLE_HPP



#ifdef unity_testing
#include <stubs/ArduinoStubs.hpp>
#include <stubs/BLE_Stubs.hpp>
#include <mock/SerialLoggerMock.hpp>
#include <makros/FMakro.hpp>
#include <types/String.h>

#include <sara_data.hpp>
#include <sara_battery.hpp>

#else
#include <Arduino.h>
#include <ArduinoBLE.h>
#include <SerialLogger.hpp>
#include <sara_data.hpp>
#include <sara_battery.hpp>
#endif


namespace sara_ble{

  enum ble_state{
    NONE,
    DISCONNECTED,
    CONNECTED
  };

  extern BLEService airService; 
  extern BLECharacteristic temperatureCharacteristic;
  extern BLECharacteristic humidityCharacteristic;
  extern BLEService weatherStationService; 
  extern BLECharacteristic rainfallCharacteristic;
  extern BLECharacteristic winddirectionCharacteristic;
  extern BLECharacteristic windspeedCharacteristic;
  extern BLEService powerService; 
  extern BLECharacteristic batterLevelCharacteristic;
  extern BLECharacteristic batterRAWCharacteristic;

  extern ble_state connection_state;

  extern String connected_device;

  void begin();

  String ble_state_to_String(ble_state state);

  void on_connect(BLEDevice central );

  void on_disconnect(BLEDevice central );

  void print_bluetooth_state();

  void update_air_data(sara_data::air_data *air_data);
  void update_weather_data(sara_data::weather_station_data *weather_data);
  void update_battery_data(sara_data::battery_data *battery_data);
}

#endif  // SARABLE_HPP

