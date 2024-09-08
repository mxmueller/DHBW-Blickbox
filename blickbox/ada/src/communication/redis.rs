use std::collections::{VecDeque, HashMap};
use futures_util::StreamExt;
use redis::AsyncCommands;
use std::sync::Arc;
use tokio::sync::Mutex;
use crate::communication::logging::logging::{LogChannel, LogEntry};

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

    pub async fn publish_all(&self) -> Result<(), redis::RedisError> {
        let mut conn = self.publish_conn.lock().await;
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

    pub async fn subscribe(&self, channel: &str) -> Result<(), redis::RedisError> {
        let mut conn = self.pubsub_conn.lock().await;
        conn.subscribe(channel).await?;
        println!("subscribing to {}", channel);
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
                println!("Received restart command on channel {}", channel);
                // Restart
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