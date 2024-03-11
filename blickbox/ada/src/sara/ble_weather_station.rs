pub mod ble_weather_station {
    use std::time::Duration;
    use btleplug::api::{bleuuid::uuid_from_u16, Central, CharPropFlags, Manager as _, Peripheral as _, ScanFilter};
    use btleplug::platform::{Manager, Peripheral};
    use tokio::time;
    use futures_util::stream::StreamExt;

    use uuid::Uuid;
    use crate::SensorData;

    // Define the UUIDs for the BLE characteristics you want to interact with
    const TEMP_NOTIFY_CHARACTERISTICS_UUID: Uuid = uuid_from_u16(0x2101);
    const HUMIDITY_NOTIFY_CHARACTERISTICS_UUID: Uuid = uuid_from_u16(0x2102);
    const RAINFALL_NOTIFY_CHARACTERISTICS_UUID: Uuid = uuid_from_u16(0x2203);
    const WIND_DIRECTION_NOTIFY_CHARACTERISTICS_UUID: Uuid = uuid_from_u16(0x2201);
    const WIND_SPEED_NOTIFY_CHARACTERISTICS_UUID: Uuid = uuid_from_u16(0x2202);
    // Define the UUID for the service containing the characteristics
    const AIR_SERVICE_UUID: Uuid = uuid_from_u16(0x1101);
    const WEATHER_STATION_SERVICE_UUID: Uuid = uuid_from_u16(0x1102);

    // gotta be 5 later on for production
    const DESIRED_NOTIFICATION_COUNT: i32 = 2;

    pub async fn get_data_ble(peripheral: Peripheral, sensor_data: &mut SensorData) -> crate::Result<()> {
        // Discover possible services from peripheral device
        peripheral.discover_services()
            .await
            .map_err(|_| String::from("Failed to discover services of peripheral"))?;

        // Find the temperature characteristics
        let temp_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|&c| c.uuid == TEMP_NOTIFY_CHARACTERISTICS_UUID && c.properties.contains(CharPropFlags::NOTIFY))
            .unwrap().clone();

        // Subscribe to temperature notification
        peripheral
            .subscribe(&temp_characteristic)
            .await
            .map_err(|_| String::from("Failed to subscribe to humidity notifications"))?;

        // Find the humidity characteristic
        let humidity_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|&c| c.uuid == HUMIDITY_NOTIFY_CHARACTERISTICS_UUID && c.properties.contains(CharPropFlags::NOTIFY))
            .unwrap().clone();

        // Subscribe humidity value
        peripheral
            .subscribe(&humidity_characteristic)
            .await
            .map_err(|_| String::from("Failed to subscribe to humidity notifications"))?;

        // Find the wind speed characteristics
        let ws_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|&c| c.uuid == WIND_SPEED_NOTIFY_CHARACTERISTICS_UUID && c.properties.contains(CharPropFlags::NOTIFY))
            .unwrap().clone();

        // Subscribe to wind speed notification
        peripheral
            .subscribe(&ws_characteristic)
            .await
            .map_err(|_| String::from("Failed to subscribe to wind speed notifications"))?;


        // Find the wind direction characteristics
        let wd_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|&c| c.uuid == WIND_DIRECTION_NOTIFY_CHARACTERISTICS_UUID && c.properties.contains(CharPropFlags::NOTIFY))
            .unwrap().clone();

        // Subscribe to wind direction notification
        peripheral
            .subscribe(&wd_characteristic)
            .await
            .map_err(|_| String::from("Failed to subscribe to wind direction notifications"))?;


        // Find the rainfall characteristics
        let rfm_characteristic = peripheral
            .characteristics()
            .iter()
            .find(|&c| c.uuid == RAINFALL_NOTIFY_CHARACTERISTICS_UUID && c.properties.contains(CharPropFlags::NOTIFY))
            .unwrap().clone();

        // Subscribe to rainfall notification
        peripheral
            .subscribe(&rfm_characteristic)
            .await
            .map_err(|_| String::from("Failed to subscribe to rainfall notifications"))?;

        // Process notifications as they are received
        let mut notification_stream = peripheral
            .notifications()
            .await
            .map_err(|_| String::from("Failed to get notification stream"))?;

        // Define a counter to limit the number of notifications processed
        let mut notification_count = 0;

        let mut got_temp_value = false;
        let mut got_hum_value = false;
        let mut got_ws_value = false;
        let mut got_wd_value = false;
        let mut got_rfm_value = false;

        // Process while the BLE connection is not broken or stopped.
        while let Some(data) = notification_stream.next().await {
            match data.uuid {
                TEMP_NOTIFY_CHARACTERISTICS_UUID => {
                    if !got_temp_value {
                        // Handle temperature notification
                        let temperature_value = data.value[0] as f32;
                        println!("Temperature: {}", temperature_value);
                        sensor_data.temperature = temperature_value;
                        notification_count += 1;
                        got_temp_value = true;
                    }
                }
                HUMIDITY_NOTIFY_CHARACTERISTICS_UUID => {
                    if !got_hum_value {
                        // Handle temperature notification
                        let humidity_value = data.value[0] as f32;
                        println!("Humidity: {}", humidity_value);
                        sensor_data.humidity = humidity_value;
                        notification_count += 1;
                        got_hum_value = true;
                    }
                }
                RAINFALL_NOTIFY_CHARACTERISTICS_UUID => {
                    if !got_rfm_value {
                        // Handle temperature notification
                        let rainfall_value = data.value[0] as f32;
                        println!("Rainfall: {}", rainfall_value);
                        sensor_data.precipitation_amount = rainfall_value;
                        notification_count += 1;
                        got_rfm_value = true;
                    }
                }
                WIND_DIRECTION_NOTIFY_CHARACTERISTICS_UUID => {
                    if !got_wd_value {
                        // Handle temperature notification
                        let wd_value = data.value[0] as f32;
                        println!("Wind direction: {}", wd_value);
                        sensor_data.wind_direction = wd_value;
                        notification_count += 1;
                        got_wd_value = true;
                    }
                }
                WIND_SPEED_NOTIFY_CHARACTERISTICS_UUID => {
                    if !got_ws_value {
                        // Handle temperature notification
                        let ws_value = data.value[0] as f32;
                        println!("Wind speed: {}", ws_value);
                        sensor_data.wind_speed = ws_value;
                        notification_count += 1;
                        got_ws_value = true;
                    }
                }
                _ => {
                    println!("Unknown data received °o°");
                }
            }
            // Check if the desired number of notifications have been processed
            if notification_count >= DESIRED_NOTIFICATION_COUNT {
                break; // Exit the loop if desired count is reached
            }
        }

        Ok(())
    }

    pub async fn connect_peripheral_device() -> crate::Result<Peripheral> {
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

        Ok(peripheral)
    }
}

