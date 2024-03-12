#include <SaraBLE.hpp>

namespace sara_ble{
    using namespace serial_logger;
    using namespace sara_data;
    using namespace sara_battery;


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
     * @brief Deklariert die SARA Bluetooth Initation mit allen Services
     * und Charakteristiken
     * 
     */
    SaraBLE::SaraBLE() : 
    airService("1101"), 
    temperatureCharacteristic("2101", BLERead | BLENotify, 16) ,
    humidityCharacteristic("2102", BLERead | BLENotify, 16),
    weatherStationService("1102"), 
    rainfallCharacteristic("2203", BLERead | BLENotify, 16),
    winddirectionCharacteristic("2201", BLERead | BLENotify, 16) ,
    windspeedCharacteristic("2202", BLERead | BLENotify, 16),
    powerService("1103"), 
    batterLevelCharacteristic("2301", BLERead | BLENotify, 16) ,
    batterRAWCharacteristic("2302", BLERead | BLENotify, 16)
    {
    }

    /**
     * @brief Initialisert und versucht eine Verbindung mit dem Bluetooth Modul
     * herzustellen.
     * 
     */
    void SaraBLE::begin(){
        
        //Setting up Bluetooth Services
        if (!BLE.begin()) {
            log(F("ble_failed:Starting BLE failed!"), ERROR);
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
        BLE.setAdvertisedService(powerService);
        powerService.addCharacteristic(batterLevelCharacteristic);
        powerService.addCharacteristic(batterRAWCharacteristic);
        BLE.addService(airService);
        BLE.addService(weatherStationService);
        BLE.addService(powerService);

        BLE.advertise();

    }

    /**
     * @brief Speichert und schreibt den aktuellen Status der Bluetooth integation
     * auf der Konsole aus
     * 
     * @param ble_device Benötigt ein BLEDevice Objekt welches im Loop erstellt wird
     */
    void SaraBLE::update_connection_state(BLEDevice *ble_device){
        if(ble_device->connected()==true){
            connection_state = CONNECTED;
            if(last_connection_state <= DISCONNECTED){
                last_connection_state = CONNECTED;
                log(F("BLE Device Connected"), INFO);
            }
            connected_device = ble_device->address();
            

        }else{
            if(last_connection_state == CONNECTED){
                last_connection_state = DISCONNECTED;
                log(F("BLE Device disconnect"), INFO);
            }
            connection_state = DISCONNECTED;
            connected_device = "";
        }
    }

    /**
     * @brief Schreibt fürs Debugging die aktuellen Bluetooth Status auf der Konsole aus
     * 
     */
    void SaraBLE::print_bluetooth_state(){
        Serial.print(F("ble_connection:"));
        Serial.println(ble_state_to_String(this->get_connection_state()));
        Serial.print(F("ble_device:"));
        Serial.println(this->get_connected_device());
    }

    /**
     * @brief Getter für den aktuellen Verbindungsstatus
     * 
     * @return ble_state 
     */
    ble_state SaraBLE::get_connection_state(){
        return connection_state;
    }

    /**
     * @brief Gibt die MAC Adresse des Verbundenen Geräts zurück
     * 
     * @return String 
     */
    String SaraBLE::get_connected_device(){
        return connected_device;
    }

    /**
     * @brief Prozess für den Hauptprogramm loop
     * 
     */
    void SaraBLE::loop(){
       BLEDevice central = BLE.central();

       update_connection_state(&central);

        if (central) 
        {
            if(central.connected()){
                temperatureCharacteristic.writeValue(weather_data.temperature);
                humidityCharacteristic.writeValue(weather_data.humidity);
                winddirectionCharacteristic.writeValue(weather_data.winddirection);
                windspeedCharacteristic.writeValue(weather_data.windspeed);
                rainfallCharacteristic.writeValue(weather_data.rainfall);
                batterRAWCharacteristic.writeValue(battery.raw_adc);
                batterLevelCharacteristic.writeValue(battery.level);
            }
        }
    }
}