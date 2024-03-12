#ifndef SARA_DATA_HPP
#define SARA_DATA_HPP

#include <Arduino.h>
#include <DHT.h>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>

namespace sara_data{
    struct weather_station_data{
        int16_t temperature;
        int16_t humidity;
        int16_t winddirection;
        int16_t windspeed;
        int16_t rainfall;
    };

    extern weather_station_data weather_data;


    void update_sensor_data(DHT *air_sensor, SFEWeatherMeterKit *weather_station);
}

#endif  // SARA_DATA_HPP