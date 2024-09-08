pub mod tests {

    #[cfg(test)]
    mod tests {
        use std::collections::VecDeque;
        use std::io::{Read, Seek, SeekFrom};

        use mockito;
        use mockito::{Matcher, Server};
        use tempfile::tempfile;
        use tokio;
        use mockall::predicate::*;
        use mockall::*;

        use crate::{SensorData, write_to_file};
        use crate::communication::http_request::http_request::{get_temp_json, send_data};
        use crate::communication::logging::logging::{log, LogEntry, LogChannel};
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

        // Testet Erstellen von Logs
        #[test]
        fn test_log() {
            let title = String::from("Test Title");
            let message = String::from("Test Message");
            let log_type = String::from("INFO");

            let log_entry = log(title.clone(), message.clone(), log_type.clone());

            assert_eq!(log_entry.title, title);
            assert_eq!(log_entry.message, message);
            assert_eq!(log_entry.log_type, log_type);
            assert!(!log_entry.timestamp.is_empty());
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

        mock! {
            pub RedisHandler {
                async fn log_to_channel(&self, channel: LogChannel, log_entry: LogEntry) -> Result<(), String>;
                async fn publish_all(&self) -> Result<(), String>;
                async fn listen(&self) -> Result<(), String>;
            }
        }

        // Testet Loggen mit Channeln
        #[tokio::test]
        async fn test_log_to_channel() {
            let mut mock_redis = MockRedisHandler::new();
            mock_redis
                .expect_log_to_channel()
                .with(eq(LogChannel::Ada), always())
                .times(1)
                .returning(|_, _| Ok(()));

            let log_entry = LogEntry {
                title: "Test".to_string(),
                message: "Test message".to_string(),
                log_type: "info".to_string(),
                timestamp: "2024-03-08 10:00:00".to_string(),
            };

            let result = mock_redis.log_to_channel(LogChannel::Ada, log_entry).await;
            assert!(result.is_ok());
        }
        #[tokio::test]
        async fn test_log_to_channel_error() {
            let mut mock_redis = MockRedisHandler::new();
            mock_redis
                .expect_log_to_channel()
                .with(eq(LogChannel::Sara), always())
                .times(1)
                .returning(|_, _| Err("Redis connection error".to_string()));

            let log_entry = LogEntry {
                title: "Test".to_string(),
                message: "Test message".to_string(),
                log_type: "error".to_string(),
                timestamp: "2024-03-08 10:00:00".to_string(),
            };

            let result = mock_redis.log_to_channel(LogChannel::Sara, log_entry).await;
            assert!(result.is_err());
            assert_eq!(result.unwrap_err(), "Redis connection error");
        }

        // Testet Publishen von den Logs
        #[tokio::test]
        async fn test_publish_all() {
            let mut mock_redis = MockRedisHandler::new();
            mock_redis
                .expect_publish_all()
                .times(1)
                .returning(|| Ok(()));

            let result = mock_redis.publish_all().await;
            assert!(result.is_ok());
        }

        // Testet Erhalten auf dem subscribed Channel
        #[tokio::test]
        async fn test_listen() {
            let mut mock_redis = MockRedisHandler::new();
            mock_redis
                .expect_listen()
                .times(1)
                .returning(|| Ok(()));

            let result = mock_redis.listen().await;
            assert!(result.is_ok());
        }

    }
}
