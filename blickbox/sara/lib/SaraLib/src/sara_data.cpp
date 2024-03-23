#include <sara_data.hpp>

namespace sara_data{
     void update_weather_station_struct(SFEWeatherMeterKit* weather_obj, weather_station_data* weather){
          weather->rainfall = round(weather_obj->getTotalRainfall()*100);
          weather->windspeed = round(weather_obj->getWindSpeed()*100);
          weather->winddirection = round(weather_obj->getTotalRainfall()*100);
     }
     void update_battery_struct(sara_battery::SaraBatteryManager* battery_obj, battery_data* battery){
          battery->raw_adc = battery_obj->read_battery_adc();
          battery->level = sara_battery::map_to_battery_level(battery->raw_adc);
          battery->voltage = sara_battery::calculate_battery_voltage(battery->raw_adc);
     }
     void update_air_struct(DHT* dht_obj, air_data* air){
          air->humidity = round(dht_obj->readHumidity() * 100);
          air->temperature = round(dht_obj->readTemperature() * 100);
     }
     
     void print_battery_data(battery_data* battery){
          Serial.print(F("Battery Data - Raw ADC: "));
          Serial.print(battery->raw_adc);
          Serial.print(F(", Level: "));
          Serial.println(battery->level);
     }
     
     void print_air_data(air_data* air){
          Serial.print(F("Air Data - Humidity: "));
          Serial.print(air->humidity);
          Serial.print(F(", Temperature: "));
          Serial.println(air->temperature);
     }
     
     void print_weather_station_data(weather_station_data* weather){
          Serial.print(F("Weather Station Data - Rainfall: "));
          Serial.print(weather->rainfall);
          Serial.print(F(", Windspeed: "));
          Serial.print(weather->windspeed);
          Serial.print(F(", Winddirection: "));
          Serial.println(weather->winddirection);
     }

}

