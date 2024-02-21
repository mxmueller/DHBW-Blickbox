#ifndef SARA_DEFINITIONS_HPP
#define SARA_DEFINITIONS_HPP

#include <Arduino.h>

namespace sara_definitions{
    struct weather_station_data{
        int16_t temperature;
        int16_t humidity;
        int16_t winddirection;
        int16_t windspeed;
        int16_t rainfall;
    };

    extern weather_station_data weather_data;
}

#endif  // SARA_DEFINITIONS_HPP