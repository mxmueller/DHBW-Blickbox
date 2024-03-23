#ifndef SARA_DATA_HPP
#define SARA_DATA_HPP

#include <Arduino.h>
#include <SparkFun_Weather_Meter_Kit_Arduino_Library.h>
#include <DHT.h>
#include <sara_battery.hpp>

using namespace sara_battery;

namespace sara_data{

    /**
     * @brief Timing für die Tasks zum Auslesen des DHT Sensors
     * 
     */
    const uint16_t AIR_TASK_TIMING = 30000;

    /**
     * @brief Timings für die Tasks zum Auslesen der Wetterstation
     * 
     */
    const uint16_t WEATHER_TASK_TIMING = 30000;

    /**
     * @brief Timing für die Tasks zum Auslesen der Batterie
     * 
     */
    const uint16_t BATTERY_TASK_TIMING = 30000;

    /**
     * @brief Datenstruktur für die Wetterstation#
     * 
     * uint16_t winddirection; in grad
     * uint16_t windspeed; in km/h
     * uint16_t rainfall; in mm
     * 
     */
    struct weather_station_data{
        uint16_t winddirection;
        uint16_t windspeed;
        uint16_t rainfall;
    };

    /**
     * @brief Datenstruktur für die Luftdaten
     * 
     * int16_t temperature; in °C
     * uint16_t humidity; in %
     * 
     */
    struct air_data{
        int16_t temperature;
        uint16_t humidity;
    };
    
    /**
     * @brief Datenstruktur für die Batteriedaten
     * 
     * uint16_t raw_adc; Rohwert des adcs
     * float voltage; in V 
     * uint8_t level; in Prozent
     * 
     */
    struct battery_data{
        uint16_t raw_adc;
        float voltage;
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
