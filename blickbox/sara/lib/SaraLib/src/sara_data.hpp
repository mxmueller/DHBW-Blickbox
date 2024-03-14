#ifndef SARA_DATA_HPP
#define SARA_DATA_HPP

#include <Arduino.h>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <DHT.h>
#include <sara_battery.hpp>

using namespace sara_battery;

namespace sara_data{

    struct weather_station_data{
        uint16_t winddirection;
        uint16_t windspeed;
        uint16_t rainfall;
    };

    struct air_data{
        int16_t temperature;
        uint16_t humidity;
    };
    
    struct battery_data{
        uint16_t raw_adc;
        uint8_t level;
    };

    void update_weather_station_struct(SFEWeatherMeterKit* , weather_station_data*);
    void update_battery_struct(SaraBatteryManager *, battery_data * );
    void update_air_struct(DHT *, air_data *);

    void print_battery_data(battery_data*);
    void print_air_data(air_data*);
    void print_weather_station_data(weather_station_data*);
}

#endif  // SARA_DATA_HPP
