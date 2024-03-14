#include <Arduino.h>
#include <SerialLogger.hpp>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <DHT.h>
#include <sara_data.hpp>
#include <sara_battery.hpp>
#include <FireTimer.h>

#if defined(NRF52_SERIES)
  #include <SaraBLE.hpp>
#endif

/**Namespaces*/
using namespace serial_communication;
using namespace serial_logger;
using namespace debugger;

using namespace sara_data;
using namespace sara_battery;
using namespace sara_ble;


/**
 * @brief  Pin Definitionen für DHT22 Sensor
*/
const int PIN_DHT = 2;
const int DHTTYPE = DHT22;

/**
 * @brief Pin Definitionen für Weather Station
*/
const int PIN_WIND_DIRECTION = A5;
const int PIN_WIND_SPEED = A6;
const int PIN_RAINFALL_SENSOR = A7;

/**
 * @brief Analog Pin an dem die Batteriespannung anliegt
 * 
 */
const int BATTERY_PIN = A4;

/**
 * @brief  Initalisierung der DHT Library
 * 
 * @return DHT 
 */
DHT dht(PIN_DHT, DHTTYPE);

/**
 * @brief Initialisieung Wetterstation Library
 * 
 * @return SFEWeatherMeterKit 
 */
SFEWeatherMeterKit weather_station(PIN_WIND_DIRECTION, PIN_WIND_SPEED, PIN_RAINFALL_SENSOR);

/**
 * @brief Deklariert den Battery Manager
 * 
 * @return SaraBatteryManager 
 */
SaraBatteryManager battery_manager (BATTERY_PIN);


/**Funktionsdefinitionen für main.cpp*/
void print_temperature();
void print_humidity();
void print_rainfall_messurement();
void print_wind_direction();
void print_wind_speed();
void print_battery_level();
void print_battery_raw();
void print_help();
void handle_serial_request();
void print_ble_state();
void update_sensor_data();


//Anlegen der Tasks
FireTimer ble_task;
FireTimer serial_task;
FireTimer air_sensor_task;
FireTimer weather_sensor_task;
FireTimer battery_status_task;

void setup() {

  // Initalisierung der Seriellen Kommunikation
  Serial.begin(115200);
  
  // Rückgabe für 
  log(F("initializing"), INFO);

  // Initalisierung des DHT22
  // Temperatur Sensors
  dht.begin();

  //Setzt die ADC Resulution auf 10 Bit
  // Da Arduino BLE 22, welcher mit nRF52840 chip 
  // ausgestattet ist über einen 10 Bit ADC verfügt.
  weather_station.setADCResolutionBits(10);

  // Initialisieung der Wetterstation
  weather_station.begin();

  // Initialisieung der Bluetooth Integration
  sara_ble::begin();

  // Rückgabe eines Ready Signals für den Benutzer der Seriellen Konsole
  log(F("Ready"), INFO);
  print_help();

  // Initialisiert den Battery Manager
  battery_manager.begin();

  // Konfigurieren der Timer
  ble_task.begin(100);
  serial_task.begin(500);
  air_sensor_task.begin(30000);
  weather_sensor_task.begin(30000);
  battery_status_task.begin(30000);
}

/**
 * Main program loop
*/
void loop() {
  
  // Aktualisiert die Sensor Daten und speichert diese in eine
  // Datenstruktur auf die die BLE Integration zugreifen kann

  // Verwaltet die BLE Integration
  if(ble_task.fire()){
    BLE.poll();

    // Energie Management falls keine Verbindung vorherscht
    switch (sara_ble::connection_state)
    {
    case DISCONNECTED:
      ble_task.update(2000);
      break;
    case CONNECTED:
      ble_task.update(200);
    }
  }


  // Verwaltet eingehende Serielle Anfragen und Kommandos
  if(serial_task.fire() && Serial.available()){
    handle_serial_message_recieved();
    handle_serial_request();
  }
  
  // Sendet neue Temperatur und Luftfeutigkeitsdaten an das BLE Central Device
  if(air_sensor_task.fire() && sara_ble::connection_state == sara_ble::CONNECTED){
    air_data air;
    update_air_struct(&dht, &air);
    sara_ble::update_air_data(&air);
  }
  
  // Sendet Batterie Level und den eigendlichen Wert vom ADC an das BLE Central Device
  if(battery_status_task.fire() && sara_ble::connection_state == sara_ble::CONNECTED){
    battery_data battery;
    update_battery_struct(&battery_manager, &battery);
    sara_ble::update_battery_data(&battery);
  }

  // Sendet neue Wetter Daten an das BLE Central Device
  if(weather_sensor_task.fire() && sara_ble::connection_state == sara_ble::CONNECTED){
    weather_station_data weather;
    update_weather_station_struct(&weather_station, &weather);
    sara_ble::update_weather_data(&weather);
  }
}



/** 
 * Verarbeitet die Kommandos, die über das Serielle Protokoll übertragen wurden
*/
void handle_serial_request(){
  if (stringComplete) {
    Serial.println(inputString);
    if(command == F("t")){
      print_temperature();
    }else if(command == F("h")){
      print_humidity();
    }else if(command == F("wd")){
      print_wind_direction();
    }else if(command == F("rfm")){
      print_rainfall_messurement();
    }else if(command == F("ws")){
      print_wind_speed();
    }else if(command == F("ble")){
      print_ble_state();
    }else if(command == F("bl")){
      print_battery_level();
    }else if(command == F("br")){
      print_battery_raw();
    }else if(command == F("help")){
      print_help();
    }
    
    stringComplete = false;
    command = "";
    inputString = "";
  }
}

/**
 * Lädt die Temperaturdaten über das OneWire Protokoll von dem 
 * DHT Temperatur sensor und überträgt diese über die Serielle Schnittstelle.
 * TODO -> Auslagerung in andere Datei
*/
void print_temperature(){
  Serial.print(F("t:"));
  Serial.println(dht.readTemperature());
}

/**
 * Lädt die Luftfeutigkeitsdaten über das OneWire Protokoll von dem 
 * DHT Temperatur sensor und überträgt diese über die Serielle Schnittstelle.
 * TODO -> Auslagerung in andere Datei
*/
void print_humidity(){
  Serial.print(F("h:"));
  Serial.println(dht.readHumidity());
}

/**
 * @brief Gibt die aktuelle windrichtung in der Konsole zurück
 * 
 */
void print_wind_direction(){
  Serial.print(F("wd:"));
  Serial.println(weather_station.getWindDirection());
}

/**
 * @brief Gibt die die aktuelle Wind Geschwindigkeit zurück
 * 
 */
void print_wind_speed(){
  Serial.print(F("ws:"));
  Serial.println(weather_station.getWindSpeed());
}

/**
 * @brief Gibt die gemessene Regenmenge über die Serielle Konolle aus
 * 
 */
void print_rainfall_messurement(){
  Serial.print(F("rfm:"));
  Serial.println(weather_station.getTotalRainfall());
}

/**
 * @brief Gibt die gemessene Regenmenge über die Serielle Konolle aus
 * 
 */
void print_battery_level(){
  battery_data battery;
  update_battery_struct(&battery_manager, &battery);
  Serial.print(F("battery_raw:"));
  Serial.println(battery.level);
}

/**
 * @brief Gibt die gemessene Regenmenge über die Serielle Konolle aus
 * 
 */
void print_battery_raw(){
  battery_data battery;
  update_battery_struct(&battery_manager, &battery);
  Serial.print(F("battery_raw:"));
  Serial.println(battery.raw_adc);
}

/**
 * @brief Gibt eine Hilfe für Benutzer des Seriellen Kosole aus
 * 
 */
void print_help(){
  Serial.println(F("h: h - humidity | t - temperature | wd - wind direction "));
  Serial.println(F("h: ws - windspeed | rfm - rainfall measurement"));
}



/**
 * @brief Ließt den aktuellen Status der Verbindung mit dem zentralen Bluetooth Gerät aus
 * 
 */
void print_ble_state(){
    Serial.print(F("ble_connection:"));
    Serial.println(ble_state_to_String(sara_ble::connection_state));
    Serial.print(F("ble_device:"));
    Serial.println(sara_ble::connected_device);
}
