#include <SaraBLE.hpp>

namespace sara_ble{
    using namespace serial_logger;
    using namespace sara_definitions;

    SaraBLE::SaraBLE() : 
    airService("1101"), 
    temperatureCharacteristic("2101", BLERead | BLENotify, 16) ,
    humidityCharacteristic("2102", BLERead | BLENotify, 16),
    weatherStationService("1102"), 
    rainfallCharacteristic("2203", BLERead | BLENotify, 16),
    winddirectionCharacteristic("2201", BLERead | BLENotify, 16) ,
    windspeedCharacteristic("2202", BLERead | BLENotify, 16)
    {
    }

    void SaraBLE::begin(){
        
        //Setting up Bluetooth Services
        if (!BLE.begin()) {
            log(F("r:ble_failed:Starting BLE failed!"), ERROR);
            while (1);
        }
        BLE.setLocalName("SARA Weather Station");
        BLE.setAdvertisedService(airService);
        airService.addCharacteristic(temperatureCharacteristic);
        airService.addCharacteristic(humidityCharacteristic);
        BLE.setAdvertisedService(weatherStationService);
        weatherStationService.addCharacteristic(winddirectionCharacteristic);
        weatherStationService.addCharacteristic(windspeedCharacteristic);
        weatherStationService.addCharacteristic(rainfallCharacteristic);
        BLE.addService(weatherStationService);
        BLE.addService(airService);

        BLE.advertise();

    }

    void SaraBLE::loop(){
       BLEDevice central = BLE.central();

        if (central) 
        {
            digitalWrite(LED_BUILTIN, HIGH);
            if(central.connected()){
                temperatureCharacteristic.writeValue(weather_data.temperature);
                humidityCharacteristic.writeValue(weather_data.humidity);
                winddirectionCharacteristic.writeValue(weather_data.winddirection);
                windspeedCharacteristic.writeValue(weather_data.windspeed);
                rainfallCharacteristic.writeValue(weather_data.rainfall);
            }
            digitalWrite(LED_BUILTIN, LOW);
        }
    }
}