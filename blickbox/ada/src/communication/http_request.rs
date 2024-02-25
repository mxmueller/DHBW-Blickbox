pub mod http_request {
    use std::time::Duration;
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
    struct PrecipitationData {
        timestamp: String,
        precipitation_amount: f32,
    }

    pub async fn send_data(sensor_data: &SensorData) -> crate::Result<()> {

        let base_url = "https://dhbwapi.maytastix.de/iot/api/insert/";


        let temp_json = get_temp_json(&sensor_data);
        let hum_json = get_humidity_json(&sensor_data);

        let data_types = vec![
            (String::from("temperature"), temp_json),
            (String::from("air-humidity"), hum_json),
            // ("wind-direction"),
            // ("wind-speed"),
            // ("precipitation-amount"),
        ];

        // Create a reqwest HTTP client
        let client = Client::new();

        for data_type in data_types.clone() {

            println!("{}", data_type.0);
            let url = format!("{}{}", base_url, data_type.0);

            let json = serde_json::to_string(&data_type.1).unwrap();
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
                    println!("Sensor data sent successfully!");
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
/*
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

    fn get_precipitation_amount_json(sensor_data: &SensorData) -> String {
        let data = PrecipitationData {
            timestamp: sensor_data.clone().timestamp,
            precipitation_amount: sensor_data.precipitation_amount,
        };
        let json = serde_json::to_string(&data).unwrap();
        return json
    }
 */

}