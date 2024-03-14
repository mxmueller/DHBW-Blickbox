#include <sara_battery.hpp>

namespace sara_battery{
   SaraBatteryManager::SaraBatteryManager(uint8_t battery_pin){
      this->battery_pin = battery_pin;
   }

   void SaraBatteryManager::begin(){
      pinMode(battery_pin, INPUT);
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
}

