#include <Arduino.h>
#include <SerialLogger.hpp>
#include <DHT.h>

/**
 * Pin Definitionen für DHT22 Sensor
*/
const int PIN_DHT = 2;
const int DHTTYPE = DHT22;

/**
 * Initalisierung der DHT Library
*/
DHT dht(PIN_DHT, DHTTYPE);

/**
 * Generierung eines Seriellen loggers
*/
SerialLogger logger;


/**Funktionsdefinitionen für main.cpp*/
void print_temperature();
void print_humidity();
void handle_serial_request();




/**Namespaces*/
using namespace serial_communication;

void setup() {
  Serial.begin(115200);
  Serial.println(F("Ello Sara here :D"));

  dht.begin();
  logger.begin();

  Serial.println(F("I am initialized!"));
  Serial.println(F("Commands: t - temp, h - humidity"));
}

/**
 * Main program loop
*/
void loop() {
  handle_serial_request();
}

/**
 * Verarbeitet die Kommandos, die über das Serielle Protokoll übertragen wurden
*/
void handle_serial_request(){
  if (stringComplete) {
    if(command == F("t")){
      print_temperature();
    }else if(command == F("h")){
      print_humidity();
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
 * Sobald daten über in den Buffer eintreffen wird ein Serial Event ausglöst
 * welches die Daten verarbeitet
*/
void serialEvent() {
  on_serial_message_recieved();
}