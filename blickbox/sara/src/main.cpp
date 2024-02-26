#include <Arduino.h>
#include <SerialLogger.hpp>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <DHT.h>
#include <sara_data.hpp>
#include <FireTimer.h>

#if defined(__arm__)
#include <SaraBLE.hpp>
#endif


/**
 * Pin Definitionen für DHT22 Sensor
*/
const int PIN_DHT = 2;
const int DHTTYPE = DHT22;

/**
 * Pin Definitionen für Weather Station
*/
const int PIN_WIND_DIRECTION = A5;
const int PIN_WIND_SPEED = A6;
const int PIN_RAINFALL_SENSOR = A7;

/**
 * Initalisierung der DHT Library
*/
DHT dht(PIN_DHT, DHTTYPE);

/**
 * @brief Initialisieung Wetterstation Library
 * 
 */
SFEWeatherMeterKit weather_station(PIN_WIND_DIRECTION, PIN_WIND_SPEED, PIN_RAINFALL_SENSOR);


/**Funktionsdefinitionen für main.cpp*/
void print_temperature();
void print_humidity();
void print_rainfall_messurement();
void print_wind_direction();
void print_wind_speed();
void print_help();
void handle_serial_request();
void print_ble_state();
void update_sensor_data();




/**Namespaces*/
using namespace serial_communication;
using namespace serial_logger;
using namespace debugger;

using namespace sara_data;

/*BLE Definitionen*/
#if defined(__arm__)
using namespace sara_ble;
SaraBLE sara_bluetooth;
#endif

FireTimer poll_timer;

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
  #if defined(__arm__)
  sara_bluetooth.begin();
  #endif

  // Rückgabe eines Ready Signals für den Benutzer der Seriellen Konsole
  log(F("Ready"), INFO);
  print_help();

  poll_timer.begin(500);
}

/**
 * Main program loop
*/
void loop() {
  
  // Aktualisiert die Sensor Daten und speichert diese in eine
  // Datenstruktur auf die die BLE Integration zugreifen kann
  update_sensor_data(&dht, &weather_station);

  // Verwaltet die BLE Integration
  #if defined(__arm__)
  sara_bluetooth.loop();
  #endif

  // Verwaltet eingehende Serielle Anfragen und Kommandos
  handle_serial_message_recieved();
  handle_serial_request();
  
  
    
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
  #if defined(__arm__)
    Serial.print(F("ble_connection:"));
    Serial.println(ble_state_to_String(sara_bluetooth.get_connection_state()));
    Serial.print(F("ble_device:"));
    Serial.println(sara_bluetooth.get_connected_device());
  #endif
  #if defined(__AVR__)
    Serial.print(F("ble_device:No BLE Device available"));
  #endif
}
