#include <Arduino.h>
#include <SerialLogger.hpp>
#include <cmdArduino.h>
#include <DHT.h>

const int PIN_DHT = 2;
const int DHTTYPE = DHT22;

DHT dht(PIN_DHT, DHTTYPE);

SerialLogger logger;

void arg_display(int argCnt, char **args);
void print_temperature(int argCnt, char **args);
void print_humidity(int argCnt, char **args);

void setup() {
  Serial.begin(115200);
  cmd.begin(115200);

  dht.begin();

  cmd.add("t", print_temperature);
  cmd.add("h", print_humidity);
  cmd.add("args", arg_display);

  logger.begin();
}

void loop() {
  cmd.poll();
}

void print_temperature(int argCnt, char **args){
  Serial.println(dht.readTemperature());
}

void print_humidity(int argCnt, char **args){
  Serial.println(dht.readHumidity());
}

void arg_display(int argCnt, char **args)
{
  for (int i=0; i<argCnt; i++)
  {
    Serial.print("Arg ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(args[i]);
  }
}