/**
 * @file sara_data.cpp
 * @brief Implementierung der Funktionen zur Aktualisierung und Ausgabe von Datenstrukturen.
 */

#include <sara_data.hpp>

namespace sara_data{

     /**
      * @brief Aktualisiert die Wetterdaten in der übergebenen Datenstruktur.
      * 
      * @param weather_obj Ein Zeiger auf das Wetterobjekt.
      * @param weather Ein Zeiger auf die Wetterdatenstruktur.
      */
     void update_weather_station_struct(SFEWeatherMeterKit* weather_obj, weather_station_data* weather){
          weather->rainfall = weather_obj->getTotalRainfall();
          weather->windspeed = weather_obj->getWindSpeed();
          weather->winddirection = weather_obj->getTotalRainfall();
     }

     /**
      * @brief Aktualisiert die Batteriedaten in der übergebenen Datenstruktur.
      * 
      * @param battery_obj Ein Zeiger auf das Batterieobjekt.
      * @param battery Ein Zeiger auf die Batteriedatenstruktur.
      */
     void update_battery_struct(sara_battery::SaraBatteryManager* battery_obj, battery_data* battery){
          battery->raw_adc = battery_obj->read_battery_adc();
          battery->voltage = sara_battery::calculate_battery_voltage(battery->raw_adc);
          battery->level = sara_battery::map_to_battery_level(battery->voltage);
     }

     /**
      * @brief Aktualisiert die Luftdaten in der übergebenen Datenstruktur.
      * 
      * @param dht_obj Ein Zeiger auf das DHT-Objekt.
      * @param air Ein Zeiger auf die Luftdatenstruktur.
      */
     void update_air_struct(DHT* dht_obj, air_data* air){
          air->humidity = dht_obj->readHumidity();
          air->temperature = dht_obj->readTemperature();
     }

     /**
      * @brief Gibt die Batteriedaten auf dem seriellen Monitor aus.
      * 
      * @param battery Ein Zeiger auf die Batteriedatenstruktur.
      */
     void print_battery_data(battery_data* battery){
          serial_logger::log("Battery Data - Raw ADC: ");
          serial_logger::log(battery->raw_adc);
          serial_logger::log(", Level: ");
          serial_logger::log(battery->level);
     }

     /**
      * @brief Gibt die Luftdaten auf dem seriellen Monitor aus.
      * 
      * @param air Ein Zeiger auf die Luftdatenstruktur.
      */
     void print_air_data(air_data* air){
          serial_logger::log("Air Data - Humidity: ");
          serial_logger::log(air->humidity);
          serial_logger::log(", Temperature: ");
          serial_logger::log(air->temperature);
     }

     /**
      * @brief Gibt die Wetterdaten der Wetterstation auf dem seriellen Monitor aus.
      * 
      * @param weather Ein Zeiger auf die Wetterdatenstruktur.
      */
     void print_weather_station_data(weather_station_data* weather){
          serial_logger::log("Weather Station Data - Rainfall: ");
          serial_logger::log(weather->rainfall);
          serial_logger::log(", Windspeed: ");
          serial_logger::log(weather->windspeed);
          serial_logger::log(", Winddirection: ");
          serial_logger::log(weather->winddirection);
     }

}

