pub mod http_request {
    use reqwest;
    use reqwest::Client;
    use serde::Serialize;
    use crate::communication::logging::logging::{log, LogChannel};
    use crate::communication::redis::redis::RedisHandler;
    use crate::SensorData;

    #[derive(Serialize, Clone, Debug)]
    struct TempData {
        timestamp: String,
        temperature: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct AirHumData {
        timestamp: String,
        air_humidity: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct WindSpeedData {
        timestamp: String,
        wind_speed: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct WindDirectionData {
        timestamp: String,
        wind_direction: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct RainData {
        timestamp: String,
        rain: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct BatteryLevel {
        timestamp: String,
        battery_charge: f32,
    }
    #[derive(Serialize, Clone, Debug)]
    struct BatteryVoltage {
        timestamp: String,
        battery_voltage: f32,
    }

    pub async fn send_data(handler: &RedisHandler, url: &str, sensor_data: &SensorData) -> crate::Result<()> {

        let base_url = url;

        let temp_json = get_temp_json(&sensor_data);
        let hum_json = get_humidity_json(&sensor_data);
        let ws_json = get_wind_speed_json(&sensor_data);
        let wd_json = get_wind_direction_json(&sensor_data);
        let rain_json = get_rain_json(&sensor_data);
        let battery_level_json = get_battery_level_json(&sensor_data);
        let battery_voltage_json = get_battery_voltage_json(&sensor_data);

        let data_types = vec![
            (String::from("temperature"), temp_json),
            (String::from("air-humidity"), hum_json),
            (String::from("wind-speed"), ws_json),
            (String::from("wind-direction"), wd_json),
            (String::from("rain"), rain_json),
            (String::from("battery-charge"), battery_level_json),
            (String::from("battery-voltage"), battery_voltage_json),
        ];

        // Create a reqwest HTTP client
        let client = Client::new();

        for data_type in data_types.clone() {
            let url = format!("{}{}", base_url, data_type.0);

            let json = data_type.1;
            println!("JSON: {} sent to <{:?}>", json, url);

            // Send the sensor data as JSON in the body of a POST request
            let response = match client.post(url)
                .header("Content-Type", "application/json")
                .header("blickbox", "true")
                .body(json)
                .send()
                .await {
                    Ok(response) => response,
                    Err(error) => {
                        return Err(format!("{}", error))
                }
            };

            match response.status().is_success() {
                true => {
                    println!("Sensor data from {} sent successfully!", data_type.0);
                    let log_message = format!("ADA sent {}", data_type.0);
                    let info_log = log(String::from("ADA"), log_message, String::from("info"));
                    handler.log_to_channel(LogChannel::Ada, info_log).await;
                }
                false => {
                    let log_message = format!("ADA could not sent {}", data_type.0);
                    let error_log = log(String::from("ADA"), log_message, String::from("error"));
                    handler.log_to_channel(LogChannel::Ada, error_log).await;
                    Err(format!("Request failed: {:?}", response.status()))?;
                }
            }
        }
        Ok(())
    }

    pub fn get_temp_json(sensor_data: &SensorData) -> String {
        let data = TempData {
            timestamp: sensor_data.clone().timestamp,
            temperature: sensor_data.temperature,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_humidity_json(sensor_data: &SensorData) -> String {
        let data = AirHumData {
            timestamp: sensor_data.clone().timestamp,
            air_humidity: sensor_data.humidity,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_wind_speed_json(sensor_data: &SensorData) -> String {
        let data = WindSpeedData {
            timestamp: sensor_data.clone().timestamp,
            wind_speed: sensor_data.wind_speed,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_wind_direction_json(sensor_data: &SensorData) -> String {
        let data = WindDirectionData {
            timestamp: sensor_data.clone().timestamp,
            wind_direction: sensor_data.wind_direction,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_rain_json(sensor_data: &SensorData) -> String {
        let data = RainData {
            timestamp: sensor_data.clone().timestamp,
            rain: sensor_data.rain,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_battery_level_json(sensor_data: &SensorData) -> String {
        let data = BatteryLevel {
            timestamp: sensor_data.clone().timestamp,
            battery_charge: sensor_data.battery_charge,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    pub fn get_battery_voltage_json(sensor_data: &SensorData) -> String {
        let data = BatteryVoltage {
            timestamp: sensor_data.clone().timestamp,
            battery_voltage: sensor_data.battery_voltage,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }
}
