pub mod redis {
    use std::collections::{HashMap, VecDeque};
    use std::env;
    use std::process::{Command, exit};
    use std::sync::Arc;
    use std::time::Duration;

    use futures_util::StreamExt;
    use redis::{AsyncCommands, RedisError};
    use tokio::sync::Mutex;

    use crate::communication::logging::logging::{handshake_log, HandshakeLog, log, LogChannel, LogEntry};

    #[derive(Clone)]
    pub struct RedisHandler {
        client: redis::Client,
        publish_conn: Arc<Mutex<redis::aio::MultiplexedConnection>>,
        pubsub_conn: Arc<Mutex<redis::aio::PubSub>>,
        logs: Arc<Mutex<HashMap<LogChannel, VecDeque<LogEntry>>>>,
    }

    impl RedisHandler {
        pub async fn new(redis_url: &str) -> Result<Self, redis::RedisError> {
            let client = redis::Client::open(redis_url)?;
            let publish_conn = client.get_multiplexed_async_connection().await?;
            let pubsub_conn = client.get_async_pubsub().await?;

            Ok(Self {
                client,
                publish_conn: Arc::new(Mutex::new(publish_conn)),
                pubsub_conn: Arc::new(Mutex::new(pubsub_conn)),
                logs: Arc::new(Mutex::new(HashMap::new())),
            })
        }

        pub async fn log_to_channel(&self, channel: LogChannel, log_entry: LogEntry) {
            let mut logs = self.logs.lock().await;
            logs.entry(channel)
                .or_insert_with(VecDeque::new)
                .push_back(log_entry);
        }

        async fn acquire_publish_conn(&self) -> Result<tokio::sync::MutexGuard<'_, redis::aio::MultiplexedConnection>, String> {
            const MAX_RETRIES: u32 = 3;
            const RETRY_DELAY: Duration = Duration::from_secs(1);

            for attempt in 1..=MAX_RETRIES {
                match self.publish_conn.try_lock() {
                    Ok(guard) => return Ok(guard),
                    Err(_) => {
                        if attempt < MAX_RETRIES {
                            eprintln!("Failed to acquire lock, retrying in {:?} (attempt {}/{})", RETRY_DELAY, attempt, MAX_RETRIES);
                            tokio::time::sleep(RETRY_DELAY).await;
                        } else {
                            return Err(format!("Failed to acquire lock after {} attempts", MAX_RETRIES));
                        }
                    }
                }
            }

            Err("Max retries reached while trying to acquire lock".to_string())
        }

        pub async fn publish_all(&self) -> Result<(), redis::RedisError> {

            let mut conn = match self.acquire_publish_conn().await {
                Ok(conn) => conn,
                Err(e) => {
                    eprintln!("Failed to acquire publish connection: {:?}", e);
                    return Err(redis::RedisError::from((redis::ErrorKind::IoError, "Failed to acquire publish connection")));
                }
            };

            let mut buffers = self.logs.lock().await;

            for (channel, buffer) in buffers.iter_mut() {
                let channel_str = match channel {
                    LogChannel::Ada => "ada-logs",
                    LogChannel::Sara => "sara-logs",
                };

                while let Some(log) = buffer.pop_front() {
                    let json = serde_json::to_string(&log).unwrap();
                    println!("Publishing to {}: {}", channel_str, json);
                    conn.publish(channel_str, json).await?;
                }
            }

            Ok(())
        }

        pub async fn publish_handshake(&self, channel_str: String, log: HandshakeLog) -> Result<(), redis::RedisError> {
            let mut conn = match self.acquire_publish_conn().await {
                Ok(conn) => conn,
                Err(e) => {
                    eprintln!("Failed to acquire publish connection: {:?}", e);
                    return Err(redis::RedisError::from((redis::ErrorKind::IoError, "Failed to acquire publish connection")));
                }
            };
            let json = serde_json::to_string(&log).unwrap();
            println!("Publishing to {}: {}", channel_str, json);
            conn.publish(channel_str, json).await?;
            Ok(())
        }

        pub async fn subscribe(&self, channel: &str) -> Result<(), redis::RedisError> {
            let mut conn = self.pubsub_conn.lock().await;
            conn.subscribe(channel).await?;
            println!("subscribed to {}", channel);
            Ok(())
        }

        pub async fn listen(&self) -> Result<(), redis::RedisError> {
            let mut conn = self.pubsub_conn.lock().await;
            let mut pubsub_stream = conn.on_message();

            while let Some(msg) = pubsub_stream.next().await {
                let payload: String = msg.get_payload()?;
                let channel: String = String::from(msg.get_channel_name());

                println!("Received message on channel {}: {}", channel, payload);

                if payload == "Restart" {
                    if channel.contains("ada") {
                        let restart_log = handshake_log(String::from("acknowledge"));
                        self.publish_handshake(String::from("ada-logs"), restart_log).await.expect("Could not send acknowledge to Redis... :(");
                        println!("Restarting ADA");
                        // TODO: Restart Logik
                        exit(0)
                    }
                    else {
                        println!("Sara has to be checked...")
                    }
                }
                if payload == "online" {
                    if channel.contains("ada") {
                        let online_log = handshake_log(String::from("online"));
                        self.publish_handshake(String::from("ada-logs"), online_log).await.expect("Could not send online status to Redis... :(");
                    }
                    else if channel.contains("sara") {
                        let online_log = handshake_log(String::from("online"));
                        self.publish_handshake(String::from("sara-logs"), online_log).await.expect("Could not send online status to Redis... :(");
                    }
                    println!("Sent online message to channel");
                }
            }

            Ok(())
        }
    }


    pub async fn initialize_redis(redis_url: &str) -> Result<RedisHandler, redis::RedisError> {
        let handler = RedisHandler::new(redis_url).await?;

        // ADA subscription
        handler.subscribe("ada").await?;

        // SARA subscription
        handler.subscribe("sara").await?;

        Ok(handler)
    }
}