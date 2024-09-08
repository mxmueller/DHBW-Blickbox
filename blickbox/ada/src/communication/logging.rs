pub mod logging {
    use serde::Serialize;
    use crate::get_time;

    #[derive(Serialize, Debug, Clone)]
    pub struct LogEntry {
        pub title: String,
        pub message: String,
        #[serde(rename = "type")]
        pub log_type: String,
        pub timestamp: String,
    }

    #[derive(Clone, Debug, Eq, Hash, PartialEq)]
    pub enum LogChannel {
        Ada,
        Sara,
    }

    pub fn log(title: String, message: String, log_type: String) -> LogEntry {
        let log_entry = LogEntry {
            title,
            message,
            log_type,
            timestamp: get_time(),
        };
        println!("Log: {:?}", log_entry);
        log_entry
    }
}
