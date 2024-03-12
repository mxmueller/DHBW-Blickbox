#ifndef SARA_BATTERY_HPP
#define SARA_BATTERY_HPP

#include <Arduino.h>

const int BATTERY_PIN = A3;

namespace sara_battery{

    struct battery_value{
        int16_t raw_adc;
        int16_t level;
    };

    extern battery_value battery;

    void update_battery_data();
}

#endif  // SARA_BATTERY_HPP