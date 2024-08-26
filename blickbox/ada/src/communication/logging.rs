pub mod logging {
    use std::collections::VecDeque;

    use reqwest;
    use reqwest::Client;
    use serde::Serialize;

    use crate::get_time;

    #[derive(Serialize, Debug)]
    pub struct LogEntry {
        pub title: String,
        pub message: String,
        #[serde(rename = "type")]
        pub log_type: String,
        pub timestamp: String,
    }

    pub async fn send_logs(url: &str, ringbuffer: &mut VecDeque<LogEntry>) -> crate::Result<()> {

        println!("received url: {}", url);
        // Create a reqwest HTTP client
        let client = Client::new();

        for log in ringbuffer {

            let json = serde_json::to_string(&log).unwrap();
            println!("JSON that will be sent: {}", json);

            // Send the logs as JSON in the body of a POST request
            let response = match client.post(url)
                .header("Content-Type", "application/json")
                .body(json)
                .send()
                .await {
                    Ok(response) => response,
                    Err(error) => {
                        return Err(format!("{}", error))
                }
            };
            println!("Response: {:?}", response);

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
        println!("Log: {:?}", log_entry);
        ringbuffer.push_back(log_entry);
    }

}