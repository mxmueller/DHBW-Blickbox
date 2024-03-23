#ifndef SARA_BATTERY_HPP
#define SARA_BATTERY_HPP

#include <Arduino.h>

/**
 * @brief Speichert den maximal anzunehmenden Wert des Analog Digital Konverters.
 * Die Batterie wird über einen Voltage Devider an den Analogen Pin angeschlossen
 * Eine LiPo Batterie hat einen Wert von 4,2 Volt wenn sie voll ist, wenn alles optimal ist.
 * Zum mappen auf den 3,3 Volt Raum wird ein Multiplikator von 0.66 verwendet (3.3/5 Volt)
 * Dabei liegt bei einer vollen Batterie 2,7 Volt auf dem Eingang an nachdem dieser durch den
 * Voltage Devider runterskaliert wurde. Bei einer eingehenden Spannung von 2,7 Volt
 * ließt der ADC einen Wert von 837 ab.
 * 
 */
const uint16_t BATTERY_MAX_READING = 840;

/**
 * @brief Speichert den minimal anzunehmenden Wert des Analog Digital Konverters
 * Bei diesem Wert sollte der LiPo Akku nicht weniger als 3 V haben. Eine entladung unter 3.27 V ist
 * schlecht für die Batterie. Nach dem Mapping auf den 3.3 V wird an dem Analogen Eingang
 * 2,11 Volt anliegen der ADC wird bei dieser Spannung einen Wert von 654 lesen.
 * 
 */
const uint16_t BATTERY_MIN_READING = 650;

const float ADC_UNITS = 1024.0F;

const float ADC_REF_VOLTAGE = 3.3F;

const uint8_t ADC_SCALE_FACTOR = 2;

namespace sara_battery{

    uint8_t map_to_battery_level(uint16_t);
    float calculate_battery_voltage(uint16_t);

    class SaraBatteryManager{
        public:
            SaraBatteryManager(uint8_t);
            void begin();
            uint16_t read_battery_adc();
            uint16_t get_last_battery_reading();
            void monitor();
        private:
            uint8_t battery_pin;
            uint16_t last_battery_reading;
    };
}

#endif  // SARA_BATTERY_HPP