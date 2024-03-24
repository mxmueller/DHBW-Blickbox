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

    const BATTERY_LEVEL_UUID: Uuid = uuid_from_u16(0x2301);

    pub async fn get_data_ble(peripheral: Peripheral, sensor_data: &mut SensorData) -> crate::Result<()> {
        // Discover possible services from peripheral device
        peripheral.discover_services()
            .await
            .map_err(|_| String::from("Failed to discover services of peripheral"))?;

        let characteristics = vec![
            TEMP_NOTIFY_CHARACTERISTICS_UUID,
            HUMIDITY_NOTIFY_CHARACTERISTICS_UUID,
            RAINFALL_NOTIFY_CHARACTERISTICS_UUID,
            WIND_DIRECTION_NOTIFY_CHARACTERISTICS_UUID,
            WIND_SPEED_NOTIFY_CHARACTERISTICS_UUID,
            BATTERY_LEVEL_UUID,
        ];

        for uuid in characteristics {

            // Find the temperature characteristics
            let characteristic = peripheral
                .characteristics()
                .iter()
                .find(|&c| c.uuid == uuid)
                .unwrap().clone();

            println!("{}", uuid);

            let sensor_value = match peripheral.read(&characteristic).await {
                Ok(value) => {
                    let low_byte = value[0] as u16;
                    let high_byte = value[1] as u16;
                    let combined_value = (high_byte << 8) | low_byte;
                    let value = combined_value as f32 / 100.0;
                    value
                }
                Err(e) => {
                    peripheral.disconnect()
                        .await
                        .map_err(|_| String::from("Failed to disconnect from peripheral"))?;
                    Err(format!("Failed to read data: {}", e))?
                }
            };

            match uuid {
                TEMP_NOTIFY_CHARACTERISTICS_UUID => {
                    println!("temp updated");
                    sensor_data.temperature = sensor_value
                }
                HUMIDITY_NOTIFY_CHARACTERISTICS_UUID => {
                    println!("hum updated");
                    sensor_data.humidity = sensor_value
                }
                RAINFALL_NOTIFY_CHARACTERISTICS_UUID => {
                    println!("rain updated");
                    sensor_data.rain = sensor_value
                }
                WIND_DIRECTION_NOTIFY_CHARACTERISTICS_UUID => {
                    println!("wd updated");
                    sensor_data.wind_direction = sensor_value
                }
                WIND_SPEED_NOTIFY_CHARACTERISTICS_UUID => {
                    println!("ws updated");
                    sensor_data.wind_speed = sensor_value
                }
                BATTERY_LEVEL_UUID => {
                    println!("battery updated");
                    sensor_data.battery_charge = sensor_value
                }
                _ => {
                    Err(String::from("Unknown data °O°"))?;
                }
            }
            println!("temp: {}, hum: {}, rain: {}", sensor_data.temperature, sensor_data.humidity, sensor_data.rain);
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

