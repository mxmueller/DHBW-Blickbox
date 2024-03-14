#include <SaraBLE.hpp>

namespace sara_ble{
    using namespace serial_logger;
    using namespace sara_data;


    /**
     * @brief Gibt die String repräsentation vom Enum zurück
     * 
     * @param state 
     * @return String 
     */
    String ble_state_to_String(ble_state state){
        switch (state)
        {
        case NONE:
            return F("NONE");
            break;
        case DISCONNECTED:
            return F("DISCONNECTED");
            break;
        case CONNECTED:
            return F("CONNECTED");
            break;
        }
    }

    ble_state connection_state = DISCONNECTED;

    String connected_device;

    BLEService airService("1101");
    BLECharacteristic temperatureCharacteristic("2101", BLERead | BLENotify, 16) ;
    BLECharacteristic humidityCharacteristic("2102", BLERead | BLENotify, 16);
    BLEService weatherStationService("1102");
    BLECharacteristic rainfallCharacteristic("2203", BLERead | BLENotify, 16);
    BLECharacteristic winddirectionCharacteristic("2201", BLERead | BLENotify, 16) ;
    BLECharacteristic windspeedCharacteristic("2202", BLERead | BLENotify, 16);
    BLEService powerService("1103");
    BLECharacteristic batterLevelCharacteristic("2301", BLERead | BLENotify, 16) ;
    BLECharacteristic batterRAWCharacteristic("2302", BLERead | BLENotify, 16);

  
    void begin(){
        
        // BLE Error Handling
        if (!BLE.begin()) {
            log(F("ble_failed:Starting BLE failed!"), ERROR);
            while (1);
        }

        // Setze Event Handler
        BLE.setEventHandler( BLEConnected, on_connect );
        BLE.setEventHandler( BLEDisconnected, on_disconnect );

        // Setze BLE Name
        BLE.setLocalName("SARA Weather Station");
        
        // Definiere BLE Services und Charakteristiken
        BLE.setAdvertisedService(airService);
        airService.addCharacteristic(temperatureCharacteristic);
        airService.addCharacteristic(humidityCharacteristic);
        BLE.setAdvertisedService(weatherStationService);
        weatherStationService.addCharacteristic(winddirectionCharacteristic);
        weatherStationService.addCharacteristic(windspeedCharacteristic);
        weatherStationService.addCharacteristic(rainfallCharacteristic);
        BLE.setAdvertisedService(powerService);
        powerService.addCharacteristic(batterLevelCharacteristic);
        powerService.addCharacteristic(batterRAWCharacteristic);
        BLE.addService(airService);
        BLE.addService(weatherStationService);
        BLE.addService(powerService);

        // Advertise Services und Charakteristiken
        BLE.advertise();
    }
    
    void on_connect(BLEDevice central ){
        connection_state = CONNECTED;
        connected_device = central.address();
        BLE.stopAdvertise();
        log(F("Device Connected"), INFO);
    }

    void on_disconnect(BLEDevice central ){
        connection_state = DISCONNECTED;
        BLE.advertise();
        log(F("Device Disconnected"), INFO);
    }
    /**
     * @brief Schreibt fürs Debugging die aktuellen Bluetooth Status auf der Konsole aus
     * 
     */
    void print_bluetooth_state(){
        Serial.print(F("ble_connection:"));
        Serial.println(ble_state_to_String(connection_state));
        Serial.print(F("ble_device:"));
        Serial.println(connected_device);
    }

    void update_air_data(sara_data::air_data *air_data) {
        temperatureCharacteristic.writeValue(air_data->temperature);
        humidityCharacteristic.writeValue(air_data->humidity);
    }

    void update_weather_data(sara_data::weather_station_data *weather_data) {
        winddirectionCharacteristic.writeValue(weather_data->winddirection);
        windspeedCharacteristic.writeValue(weather_data->windspeed);
        rainfallCharacteristic.writeValue(weather_data->rainfall);
    }

    void update_battery_data(sara_data::battery_data *battery_data) {
        batterRAWCharacteristic.writeValue(battery_data->raw_adc);
        batterLevelCharacteristic.writeValue(battery_data->level);
    }

    // if(central.connected()){
    //     update_air_data(&air_data);
    //     update_weather_data(&weather_data);
    //     update_battery_data(&battery_data);
    // }
            // if(central.connected()){
            //     temperatureCharacteristic.writeValue(weather_data.temperature);
            //     humidityCharacteristic.writeValue(weather_data.humidity);
            //     winddirectionCharacteristic.writeValue(weather_data.winddirection);
            //     windspeedCharacteristic.writeValue(weather_data.windspeed);
            //     rainfallCharacteristic.writeValue(weather_data.rainfall);
            //     batterRAWCharacteristic.writeValue(battery.raw_adc);
            //     batterLevelCharacteristic.writeValue(battery.level);

}