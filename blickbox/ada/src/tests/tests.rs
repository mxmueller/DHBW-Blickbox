pub mod tests {

    #[cfg(test)]
    mod tests {
        use std::collections::VecDeque;
        use std::io::{Read, Seek, SeekFrom};

        use mockito;
        use mockito::{Matcher, Server};
        use tempfile::tempfile;
        use tokio;

        use crate::{SensorData, write_to_file};
        use crate::communication::http_request::http_request::{get_temp_json, send_data, send_last_online};
        use crate::communication::logging::logging::{log, LogEntry, send_logs};
        use crate::tests::mocking_sensor_data::mocking_sensor_data::generate_mock_sensor_data;

        // Testet Schreiben in Datei
        #[test]
        fn test_write_to_file() {
            // Temporäre Datei
            let mut temp_file = tempfile().unwrap();

            let sensor_data = SensorData {
                timestamp: "2024-02-23 19:32:23".to_string(),
                temperature: 27.4,
                humidity: 55.0,
                wind_speed: 10.2,
                wind_direction: 270.0,
                rain: 0.0,
                battery_charge: 75.0,
                battery_voltage: 3.7,
            };

            write_to_file(&mut temp_file, &sensor_data);

            temp_file.seek(SeekFrom::Start(0)).unwrap();

            let mut content = String::new();
            temp_file.read_to_string(&mut content).unwrap();

            let expected_data = format!("{:?}\n", sensor_data);
            assert_eq!(content, expected_data);
        }


        // Testet senden von Logs an API
        #[tokio::test]
        async fn test_send_logs() {
            let mut server = Server::new_async().await;

            // Mock für die POST-Anfrage zu /ada-logs
            let _m = server.mock("POST", "/ada-logs")
                .with_status(200)
                .with_body("ok")
                .create_async()
                .await;
            let base_url = server.url();
            let url = format!("{}/ada-logs", base_url);

            let mut ringbuffer: VecDeque<LogEntry> = VecDeque::new();
            log(String::from("Test"), String::from("This is a test log"), String::from("info"), &mut ringbuffer);

            let result = send_logs(&url, &mut ringbuffer).await;
            println!("Result of test_send_logs: {:?}", result);

            assert!(result.is_ok());
        }
        #[tokio::test]
        async fn test_send_logs_failure() {
            let mut server = Server::new_async().await;

            // Mock für Fehlerstatuscode
            let _m = server.mock("POST", "/ada-logs")
                .with_status(500)
                .with_body("error")
                .create_async()
                .await;
            let base_url = server.url();
            let url = format!("{}/ada-logs", base_url);

            let mut ringbuffer: VecDeque<LogEntry> = VecDeque::new();
            log(String::from("Test"), String::from("This is a test log"), String::from("info"), &mut ringbuffer);

            let result = send_logs(&url, &mut ringbuffer).await;
            println!("Result of test_send_logs: {:?}", result);

            assert!(result.is_err());
        }

        // Testet Erstellen von Logs
        #[test]
        fn test_log() {
            let mut ringbuffer: VecDeque<LogEntry> = VecDeque::new();
            let title = String::from("Test Title");
            let message = String::from("Test Message");
            let log_type = String::from("INFO");

            log(title.clone(), message.clone(), log_type.clone(), &mut ringbuffer);

            assert_eq!(ringbuffer.len(), 1);
            let log_entry = ringbuffer.pop_back().unwrap();

            assert_eq!(log_entry.title, title);
            assert_eq!(log_entry.message, message);
            assert_eq!(log_entry.log_type, log_type);
            assert!(!log_entry.timestamp.is_empty());
        }

        // Testet Senden eines Zuletzt-Online-Status
        #[tokio::test]
        async fn test_send_last_online_success() {
            let mut server = Server::new_async().await;

            // Mock für die POST-Anfrage zu /last-online
            let _m = server.mock("POST", "/pingBB")
                .with_status(200)
                .with_body("ok")
                .create_async().await;

            let base_url = server.url();
            let url = format!("{}/pingBB", base_url);

            let result = send_last_online(&url).await;
            println!("Result of test_send_last_online_success: {:?}", result);

            assert!(result.is_ok());
        }
        #[tokio::test]
        async fn test_send_last_online_failure() {
            let mut server = Server::new_async().await;

            // Mock für die POST-Anfrage zu /last-online mit einem Fehlerstatuscode
            let _m = server.mock("POST", "/pingBB")
                .with_status(500)
                .with_body("error")
                .create_async().await;

            let base_url = server.url();
            let url = format!("{}/pingBB", base_url);

            let result = send_last_online(&url).await;
            println!("Result of test_send_last_online_failure: {:?}", result);

            assert!(result.is_err());
        }

        // Testet Senden von Sensordaten
        #[tokio::test]
        async fn test_send_data_success() {
            let mut server = Server::new_async().await;

            // Mocks für die POST-Anfragen zu verschiedenen Sensor-Daten
            let endpoints = vec![
                String::from("temperature"),
                String::from("air-humidity"),
                String::from("wind-speed"),
                String::from("wind-direction"),
                String::from("rain"),
                String::from("battery-charge"),
                String::from("battery-voltage"),
            ];
            let regex = format!("^/({})$", endpoints.join("|"));
            let formatting_regex = format!(r"{}", regex).to_string();

            server.mock("POST", Matcher::Regex(formatting_regex))
                .with_status(200)
                .with_body("ok")
                .create_async().await;

            let base_url = server.url();

            let sensor_data = generate_mock_sensor_data();

            let result = send_data(&base_url, &sensor_data).await;
            println!("Result of test_send_data_success: {:?}", result);

            assert!(result.is_ok());
        }
        #[tokio::test]
        async fn test_send_data_failure() {
            let mut server = Server::new_async().await;

            let endpoints = vec![
                "temperature",
                "air-humidity",
                "wind-speed",
                "wind-direction",
                "rain",
                "battery-charge",
                "battery-voltage"
            ];
            let regex = format!("^/({})$", endpoints.join("|"));
            let formatting_regex = format!(r"{}", regex).to_string();

            server.mock("POST", Matcher::Regex(formatting_regex))
                .with_status(500)
                .with_body("error")
                .create_async().await;


            let base_url = server.url();

            let sensor_data = generate_mock_sensor_data();

            let result = send_data(&base_url, &sensor_data).await;
            println!("Result of test_send_data_failure: {:?}", result);

            assert!(result.is_err());
        }

        // Testet Erstellen von JSON-Objekten aus SensorData-Struct
        #[test]
        fn test_get_json() {
            let expected_temp_json = String::from("{\"timestamp\":\"2024-02-23 19:32:23\",\"temperature\":27.4}");

            let sensor_data = SensorData {
                timestamp: String::from("2024-02-23 19:32:23"),
                temperature: 27.4,
                humidity: 0.0,
                wind_speed: 0.0,
                wind_direction: 0.0,
                rain: 0.0,
                battery_charge: 0.0,
                battery_voltage: 0.0,
            };

            assert_eq!(get_temp_json(&sensor_data), expected_temp_json)
        }
        #[test]
        fn test_get_json_failure() {
            let expected_temp_json = String::from("{\"timestamp\":\"2024-02-23 19:32:23\",\"temperature\":25.0}");

            let sensor_data = SensorData {
                timestamp: String::from("2024-02-23 19:32:23"),
                temperature: 27.4, // Falsche Temperatur
                humidity: 0.0,
                wind_speed: 0.0,
                wind_direction: 0.0,
                rain: 0.0,
                battery_charge: 0.0,
                battery_voltage: 0.0,
            };

            assert_ne!(get_temp_json(&sensor_data), expected_temp_json);
        }
    }
}
