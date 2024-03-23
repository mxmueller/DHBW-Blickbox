pub mod http_request {
    use reqwest;
    use reqwest::Client;
    use serde::Serialize;
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
    struct Battery {
        timestamp: String,
        battery_charge: f32,
    }

    pub async fn send_last_online() -> crate::Result<()> {

        let url = " https://dhbwapi.maytastix.de/iot/api/pingBB";

        // Create a reqwest HTTP client
        let client = Client::new();

            // Send the sensor data as JSON in the body of a POST request
            let response = client.post(url)
                .send()
                .await
                .map_err(|error| format!("Failed to send request: {:?}", error))?;

            match response.status().is_success() {
                true => {
                    println!("Last Online Status sent successfully!");
                }
                false => {
                    Err(format!("Request failed: {:?}", response.status()))?;
                }
            }
        Ok(())
    }

    pub async fn send_data(sensor_data: &SensorData) -> crate::Result<()> {

        let base_url = "https://dhbwapi.maytastix.de/iot/api/insert/";

        let temp_json = get_temp_json(&sensor_data);
        let hum_json = get_humidity_json(&sensor_data);
        let ws_json = get_wind_speed_json(&sensor_data);
        let wd_json = get_wind_direction_json(&sensor_data);
        let rain_json = get_rain_json(&sensor_data);
        let battery_json = get_battery_json(&sensor_data);

        let data_types = vec![
            (String::from("temperature"), temp_json),
            (String::from("air-humidity"), hum_json),
            (String::from("wind-speed"), ws_json),
            (String::from("wind-direction"), wd_json),
            (String::from("rain"), rain_json),
            (String::from("battery-charge"), battery_json),
        ];

        // Create a reqwest HTTP client
        let client = Client::new();

        for data_type in data_types.clone() {

            let url = format!("{}{}", base_url, data_type.0);

            let json = data_type.1;
            println!("JSON: {} sent to <{:?}>", json, url);

            // Send the sensor data as JSON in the body of a POST request
            let response = client.post(url)
                .header("Content-Type", "application/json")
                .body(json)
                .send()
                .await
                .map_err(|error| format!("Failed to send request: {:?}", error))?;

            match response.status().is_success() {
                true => {
                    println!("Sensor data from {} sent successfully!", data_type.0);
                }
                false => {
                    Err(format!("Request failed: {:?}", response.status()))?;
                }
            }
        }
        Ok(())
    }

    fn get_temp_json(sensor_data: &SensorData) -> String {
        let data = TempData {
            timestamp: sensor_data.clone().timestamp,
            temperature: sensor_data.temperature,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    fn get_humidity_json(sensor_data: &SensorData) -> String {
        let data = AirHumData {
            timestamp: sensor_data.clone().timestamp,
            air_humidity: sensor_data.humidity,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    fn get_wind_speed_json(sensor_data: &SensorData) -> String {
        let data = WindSpeedData {
            timestamp: sensor_data.clone().timestamp,
            wind_speed: sensor_data.wind_speed,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }
        fn get_wind_direction_json(sensor_data: &SensorData) -> String {
        let data = WindDirectionData {
            timestamp: sensor_data.clone().timestamp,
            wind_direction: sensor_data.wind_direction,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    fn get_rain_json(sensor_data: &SensorData) -> String {
        let data = RainData {
            timestamp: sensor_data.clone().timestamp,
            rain: sensor_data.rain,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    fn get_battery_json(sensor_data: &SensorData) -> String {
        let data = Battery {
            timestamp: sensor_data.clone().timestamp,
            battery_charge: sensor_data.battery_charge,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }

    #[cfg(test)]
    mod test {
        use std::time::SystemTime;
        use chrono::{DateTime, Utc};
        use chrono_tz::Europe::Berlin;

        use super::*;

        # [test]
        fn test_get_json() {
            let date_time_format: DateTime<Utc> = SystemTime::now().into();
            let time = date_time_format.with_timezone(&Berlin).format("%Y-%m-%d %H:%M:%S").to_string();

            let expected_temp_json = String::from("{\"timestamp\":\"2024-02-23 19:32:23\",\"temperature\":27.4}");

            let sensor_data = SensorData {
                timestamp: String::from("2024-02-23 19:32:23"),
                temperature: 27.4,
                humidity: 0.0,
                wind_speed: 0.0,
                wind_direction: 0.0,
                rain: 0.0,
            };

            assert_eq!(get_temp_json(&sensor_data), expected_temp_json)
        }
    }

}


