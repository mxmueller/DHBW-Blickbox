pub mod http_request {
    use std::collections::VecDeque;
    use reqwest;
    use reqwest::Client;
    use serde::Serialize;
    use crate::{get_time};

    #[derive(Serialize)]
    pub struct LogEntry {
        title: String,
        message: String,
        log_type: String,
        timestamp: String,
    }


    pub async fn send_logs(ringbuffer: &mut VecDeque<LogEntry>) -> crate::Result<()> {

        let url = "https://dhbwapi.maytastix.de/log-stream";
        // Create a reqwest HTTP client
        let client = Client::new();

        for log in ringbuffer {

            let json = serde_json::to_string(&log).unwrap();
            println!("{}", json);

            // Send the logs as JSON in the body of a POST request
            let response = client.post(url)
                .header("Content-Type", "application/json")
                .body(json)
                .send()
                .await
                .map_err(|error| format!("Failed to send request: {:?}", error))?;

            match response.status().is_success() {
                true => {
                    println!("Logs sent successfully!");
                }
                false => {
                    Err(format!("Request failed: {:?}", response.status()))?;
                }
            }
        }
        Ok(())
    }

    pub fn log(title: String, message: String, log_type: String, ringbuffer: &mut VecDeque<LogEntry>) {
        let log_entry = LogEntry {
            title,
            message,
            log_type,
            timestamp: get_time(),
        };
        ringbuffer.push_back(log_entry);
    }

}