#include <sara_battery.hpp>

#include <SerialLogger.hpp>
namespace sara_battery{
   SaraBatteryManager::SaraBatteryManager(uint8_t battery_pin){
      this->battery_pin = battery_pin;
   }

   void SaraBatteryManager::begin(){
      pinMode(battery_pin, INPUT);
      // Deaktivieren von Powerled und i2c Sensoren
      pinMode(PIN_ENABLE_SENSORS_3V3, OUTPUT);
      pinMode(PIN_ENABLE_I2C_PULLUP, OUTPUT);
      digitalWrite(PIN_ENABLE_SENSORS_3V3, LOW); 
      digitalWrite(PIN_ENABLE_I2C_PULLUP, LOW);
      digitalWrite(LED_PWR,LOW);  
   }
   
   uint16_t SaraBatteryManager::read_battery_adc(){
      last_battery_reading = analogRead(battery_pin);
      return last_battery_reading;
   }

   uint16_t SaraBatteryManager::get_last_battery_reading(){
      return last_battery_reading;
   }

   uint8_t map_to_battery_level(uint16_t raw_battery_value){
      return map(raw_battery_value, BATTERY_MIN_READING, BATTERY_MAX_READING, 0, 100);
   }
   float calculate_battery_voltage(uint16_t raw_battery_value){
      float mVPerUnit = ADC_REF_VOLTAGE / ADC_UNITS;
      float battery_voltage = raw_battery_value * mVPerUnit * ADC_SCALE_FACTOR;
      serial_logger::log("mVPerUnit: " + String(mVPerUnit), debugger::DEBUG);
      serial_logger::log("battery_voltage: " + String(battery_voltage), debugger::DEBUG);
      serial_logger::log("adc_value: " + String(raw_battery_value), debugger::DEBUG);
      return raw_battery_value * mVPerUnit * ADC_SCALE_FACTOR;
   }

   void monitor(){

   }
}

