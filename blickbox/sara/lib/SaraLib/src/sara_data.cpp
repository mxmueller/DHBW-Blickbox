#include <sara_data.hpp>

namespace sara_data{
     weather_station_data weather_data;

     /**
      * @brief Speichert die Daten aus den Sensor Bibliotheken und speichert diese
      * in die Datenstruktur weather_data
      * 
      * @param air_sensor 
      * @param weather_station 
      */
     void update_sensor_data(DHT *air_sensor, SFEWeatherMeterKit *weather_station){
          weather_data.humidity = air_sensor->readHumidity();
          weather_data.temperature = air_sensor->readTemperature();
          weather_data.winddirection = weather_station->getWindDirection();
          weather_data.rainfall = weather_station->getTotalRainfall();
          weather_data.windspeed = weather_station->getWindSpeed();
     }
}

