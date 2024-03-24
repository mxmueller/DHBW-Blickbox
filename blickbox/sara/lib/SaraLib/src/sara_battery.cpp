#include <sara_battery.hpp>


namespace sara_battery{

   /**
    * @brief Deklariert den Battery Manager und den Pin auf dem die Batteriespannung anliegt
    * 
    * @param battery_pin 
    */
   SaraBatteryManager::SaraBatteryManager(uint8_t battery_pin){
      this->battery_pin = battery_pin;
   }

   /**
    * @brief Initialisiert den Battery Manager und setzt 
    * Sparmaßnahmen um den Stromverbrauch zu reduzieren.
    * 
    */
   void SaraBatteryManager::begin(){
      pinMode(battery_pin, INPUT);
      // Deaktivieren von Powerled und i2c Sensoren
      pinMode(PIN_ENABLE_SENSORS_3V3, OUTPUT);
      pinMode(PIN_ENABLE_I2C_PULLUP, OUTPUT);
      digitalWrite(PIN_ENABLE_SENSORS_3V3, LOW); 
      digitalWrite(PIN_ENABLE_I2C_PULLUP, LOW);
      digitalWrite(LED_PWR,LOW);  
   }
   
   /**
    * @brief Ließt den ADC Wert der Batteriespannung
    * 
    * @return uint16_t 
    */
   uint16_t SaraBatteryManager::read_battery_adc(){
      last_battery_reading = analogRead(battery_pin);
      return last_battery_reading;
   }

   /**
    * @brief Gibt den zuvor gemessenen Wert der Batteriespannung zurück
    * 
    * @return uint16_t 
    */
   uint16_t SaraBatteryManager::get_last_battery_reading(){
      return last_battery_reading;
   }

   /**
    * @brief Nutzt eine Tabelle um die Batteriespannung in Prozent umzurechnen.
    * 
    * @param battery_voltage 
    * @return uint8_t 
    */
   uint8_t map_to_battery_level(float battery_voltage){
      int level = 0; // angenommen, volle Ladung
      uint16_t array_size = sizeof(BATTERY_VOLTAGE_1S) / sizeof(float);
      for (u_int16_t i = 0; i < array_size; ++i) {
         if (battery_voltage >= BATTERY_VOLTAGE_1S[i]) {
               break;
         }
         level += 5; 
      }
      return level;
   }
   

   /**
    * @brief Berechnet die Batteriespannung anhand von dem Wert aus dem Analog Digital Converter
    * Hierfür wird ein Spannungsteiler mit 2x 100kOhm verwendet, damit kann die Spannung von 0-4,2V gemessen werden.
    * und ist für Systeme mit einer Betriebsspannung von 3,3V geeignet. Je nachdem welche Wiederstände verwendet werden
    * kann sich die Toleranz unterscheiden.
    * 
    * Aufbau des Spannungsteilers:
    * GND ---- 100 kOhm ---- ADC ---- 100 kOhm ---- VBAT
    * 
    * @param raw_battery_value ADC Wert
    * @return float Wert der Batteriespannung mit einer Genauigkeit von 1 Nachkommastellen
    */
   float calculate_battery_voltage(uint16_t raw_battery_value){
      float mVPerUnit = ADC_REF_VOLTAGE / ADC_UNITS;
      float battery_voltage = raw_battery_value * mVPerUnit * ADC_SCALE_FACTOR;
      return battery_voltage;
   }

   void monitor(){

   }
}

