#ifndef SARA_BATTERY_HPP
#define SARA_BATTERY_HPP

#include <Arduino.h>
#include <SerialLogger.hpp>
#include <voltage_to_capacity_table.hpp>


namespace sara_battery{

    /**
     * @brief Definiert den maximalen ADC Wert
     * Dieser lässt sich aus der Auflösung des ADCs berechnen.
     * Auf dem nrf52840 beträgt die Auflösung 10 Bit.
     * Dieser kann auch auf 12 Bit erhöht werden.
     * 
     */
    const float ADC_UNITS = 1024.0F;

    /**
     * @brief Definiert die Referenzspannung des ADCs
     * Auf dem nr52840 beträgt die Referenzspannung 3,3V
     * 
     */
    const float ADC_REF_VOLTAGE = 3.3F;

    /**
     * @brief Da ein Spannungsteiler verwendet wird, muss der Wert des ADCs umgerechnet werden.
     * Der Spannungsteiler besteht aus 2x 100kOhm Wiederständen. Somit beträgt der Skalierungsfaktor 2.
     * 
     */
    const uint8_t ADC_SCALE_FACTOR = 2;

    /**
     * @brief Mappt einen Wert auf den Batteriestand.
     *
     * Diese Funktion mappt einen gegebenen Wert auf den entsprechenden Batteriestand.
     *
     * @param value Der zu mappende Wert.
     * @return Der gemappte Batteriestand als uint8_t in Prozent.
     */
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