pub mod ble_weather_station {
    use std::time::Duration;
    use btleplug::api::{bleuuid::uuid_from_u16, Central, Manager as _, Peripheral as _, ScanFilter};
    use btleplug::platform::{Adapter, Manager, Peripheral};
    use tokio::time;

    use uuid::Uuid;

    pub async fn get_data_ble() -> crate::Result<()> {
        // Initialize the Bluetooth manager
        let manager = Manager::new().await.unwrap();

        // Get the first Bluetooth adapter available
        let adapters = manager.adapters()
            .await
            .map_err(|_| String::from("Failed to get an available Bluetooth adapter"))?;

        let adapter = match adapters.into_iter().nth(0) {
            Some(adapter) => adapter,
            None => Err(String::from("No Bluetooth adapter found"))?,
        };

        // Start scanning for Bluetooth devices
        adapter.start_scan(ScanFilter::default())
            .await
            .map_err(|_| String::from("Failed to start scanning Bluetooth devices"))?;
        time::sleep(Duration::from_secs(2)).await;

        //find the device we're interested in which would be saras services

        // Define the UUIDs for the BLE characteristics you want to interact with
        let temperature_uuid: Uuid = uuid_from_u16(0x2101);
        let humidity_uuid = uuid_from_u16(0x2102);
        // Define the UUID for the service containing the characteristics
        let service_uuid = uuid_from_u16(0x1101);

        // Connect to a peripheral device offering the desired service
        let peripheral = match adapter.peripherals().await {
            Ok(peripherals) => {
                let mut peripheral_found = None;
                for p in peripherals {
                    if p.properties()
                        .await
                        .unwrap()
                        .unwrap()
                        .local_name
                        .iter()
                        .any(|name| name.contains("SARA Weather Station"))
                    {
                        peripheral_found = Some(p);
                        break;
                    }
                }
                peripheral_found.ok_or("Peripheral not found")?
            }
            Err(e) => {
                Err(format!("could not initialize peripheral: {}", e))?
            }
        };

        // Connect to the peripheral
        peripheral.connect()
            .await
            .map_err(|_| String::from("Failed to connect to peripheral"))?;
        // Discover possible services from peripheral device
        peripheral.discover_services()
            .await
            .map_err(|_| String::from("Failed to discover services of peripheral"))?;

        // Find the temperature characteristics
        let temp_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|c| c.uuid == temperature_uuid)
            .unwrap().clone();

        // Find the humidity characteristic
        let humidity_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|c| c.uuid == humidity_uuid)
            .unwrap().clone();

        // Read temperature value
        let temperature_value = peripheral.read(&temp_characteristic)
            .await
            .map_err(|_| String::from("Failed to read temperature value"))?;

        // Read humidity value
        let humidity_value = peripheral.read(&humidity_characteristic)
            .await
            .map_err(|_| String::from("Failed to read humidity value"))?;

        // Convert the values to appropriate types (assuming they are encoded appropriately)

        println!("Temperature: {:?}", temperature_value);
        println!("Humidity: {:?}", humidity_value);

        // Disconnect from the peripheral
        peripheral.disconnect()
            .await
            .map_err(|_| String::from("Failed to disconnect from peripheral"))?;

        Ok(())
    }
}

