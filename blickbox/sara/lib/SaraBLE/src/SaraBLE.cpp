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

    /**
     * @brief Speichert den aktuellen Bluetooth Verbindungs Status
     * 
     */
    ble_state connection_state = DISCONNECTED;

    /**
     * @brief Speichert die MAC Adresse des verbundenen Geräts
     * 
     */
    String connected_device;

    // Definiere BLE Services und Charakteristiken
    BLEService airService("1101");
    BLECharacteristic temperatureCharacteristic("2101", BLERead | BLENotify, 16) ;
    BLECharacteristic humidityCharacteristic("2102", BLERead | BLENotify, 16);
    BLEService weatherStationService("1102");
    BLECharacteristic rainfallCharacteristic("2203", BLERead | BLENotify, 16);
    BLECharacteristic winddirectionCharacteristic("2201", BLERead | BLENotify, 16) ;
    BLECharacteristic windspeedCharacteristic("2202", BLERead | BLENotify, 16);
    BLEService powerService("1103");
    BLECharacteristic batterLevelCharacteristic("2301", BLERead | BLENotify, 16) ;
    BLECharacteristic batterVoltageCharacteristic("2302", BLERead | BLENotify, 16);

  
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
        powerService.addCharacteristic(batterVoltageCharacteristic);
        BLE.addService(airService);
        BLE.addService(weatherStationService);
        BLE.addService(powerService);

        // Advertise Services und Charakteristiken
        BLE.advertise();
    }
    
    /**
     * @brief Connect Event Handler setzt den Bluetooth Status auf CONNECTED und
     * speichert die MAC Adresse des verbundenen Geräts und stoppt das Advertisen der Services
     * 
     * @param central 
     */
    void on_connect(BLEDevice central ){
        connection_state = CONNECTED;
        connected_device = central.address();
        BLE.stopAdvertise();
        log(F("Device Connected"), INFO);
    }

    /**
     * @brief Disconnect Event Handler setzt den Bluetooth Status auf DISCONNECTED und
     * startet das Advertisen der Services
     * 
     * @param central 
     */
    void on_disconnect(BLEDevice central ){
        connection_state = DISCONNECTED;
        connected_device = "";
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

    /**
     * @brief Aktualisiert die Luftdaten in den BLE Charakteristiken
     * wenn das Gerät mit einem Notification Handler verbunden ist 
     * wird diese über neue Daten informiert. Wandelt die Floats in Ints um indem es
     * die Werte mit 100 multipliziert und rundet.
     * 
     * @param air_data 
     */
    void update_air_data(sara_data::air_data *air_data) {
        uint16_t temperature = round(air_data->temperature * 100);
        uint16_t humidity = round(air_data->humidity * 100);

        temperatureCharacteristic.writeValue(temperature);
        humidityCharacteristic.writeValue(humidity);
    }

    /**
     * @brief Aktualisiert die Wetterdaten in den BLE Charakteristiken
     * wenn das Gerät mit einem Notification Handler verbunden ist 
     * wird diese über neue Daten informiert. Wandelt die Floats in Ints um indem es
     * die Werte mit 100 multipliziert und rundet.
     * 
     * @param weather_data 
     */
    void update_weather_data(sara_data::weather_station_data *weather_data) {
        uint16_t winddirection = round(weather_data->winddirection * 100);
        uint16_t windspeed = round(weather_data->windspeed * 100);
        uint16_t rainfall = round(weather_data->rainfall * 100);

        winddirectionCharacteristic.writeValue(winddirection);
        windspeedCharacteristic.writeValue(windspeed);
        rainfallCharacteristic.writeValue(rainfall);
    }

    /**
     * @brief Aktualisiert die Batteriedaten in den BLE Charakteristiken
     * wenn das Gerät mit einem Notification Handler verbunden ist 
     * wird diese über neue Daten informiert. Wandelt das Batterielevel in ein Int um indem es
     * die Werte mit 100 multipliziert und rundet.
     * 
     * @param battery_data 
     */
    void update_battery_data(sara_data::battery_data *battery_data) {
        int16_t battery_voltage = round(battery_data->voltage * 100);

        batterVoltageCharacteristic.writeValue(battery_voltage);
        batterLevelCharacteristic.writeValue(battery_data->level);
    }
}