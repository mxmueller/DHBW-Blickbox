#include <Arduino.h>
#include <SerialLogger.hpp>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <DHT.h>

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

/**
 * Generierung eines Seriellen loggers
*/
SerialLogger logger;


/**Funktionsdefinitionen für main.cpp*/
void print_temperature();
void print_humidity();
void print_rainfall_messurement();
void print_wind_direction();
void print_wind_speed();
void print_help();
void handle_serial_request();




/**Namespaces*/
using namespace serial_communication;

void setup() {

  // Initalisierung der Seriellen Kommunikation
  Serial.begin(115200);
  
  //Blockiert solange die Serielle Schnittstelle nicht Initalisiert ist
  while(!Serial);

  Serial.println("i: waiting");

  logger.begin();

  // Initalisierung des DHT22
  // Temperatur Sensors
  dht.begin();

  //Setzt die ADC Resulution auf 12 Bit
  // Da Arduino BLE 22, welcher mit nRF52840 chip 
  // ausgestattet ist über einen 12 Bit ADC verfügt.
  weather_station.setADCResolutionBits(10);

  // Initialisieung der Wetterstation
  weather_station.begin();

  Serial.println(F("i: ready"));
  print_help();
}

/**
 * Main program loop
*/
void loop() {
  on_serial_message_recieved();
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
    }else {
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

void print_wind_direction(){
  Serial.print(F("wd:"));
  Serial.println(weather_station.getWindDirection());
}


void print_wind_speed(){
  Serial.print(F("ws:"));
  Serial.println(weather_station.getWindSpeed());
}


void print_rainfall_messurement(){
  Serial.print(F("rfm:"));
  Serial.println(weather_station.getTotalRainfall());
}

void print_help(){
  Serial.println(F("c: h - humidity | t - temperature | wd - wind direction "));
  Serial.println(F("c: ws - windspeed | rfm - rainfall measurement"));
}