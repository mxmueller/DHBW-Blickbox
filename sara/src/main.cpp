#include <Arduino.h>
#include <SerialLogger.hpp>
#include <DHT.h>

const int PIN_DHT = 2;
const int DHTTYPE = DHT22;

DHT dht(PIN_DHT, DHTTYPE);

SerialLogger logger;

void print_temperature();
void print_humidity();

using namespace SerialCommunication;



void setup() {
  Serial.begin(115200);
  Serial.println("Ello Sara here :D");
  dht.begin();

  logger.begin();
  Serial.println(F("I am initialized!"));
  Serial.println(F("Commands: t - temp, h - humidity"));
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString);
    if(command == "t"){
      print_temperature();
    }else if(command == "h"){
      print_humidity();
    }
    // clear the string:
    stringComplete = false;
    command = "";
    inputString = "";
}
}

void print_temperature(){
  Serial.print("t:");
  Serial.println(dht.readTemperature());
}

void print_humidity(){
  Serial.print("h:");
  Serial.println(dht.readHumidity());
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  Handle_Serial_Request();
}