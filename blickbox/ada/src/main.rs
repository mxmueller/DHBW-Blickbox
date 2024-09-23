use std::fs::{File, OpenOptions};
use std::io::{Write};
use std::time::{Duration, SystemTime};

use btleplug::api::Peripheral;
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use serde::Serialize;
use tokio::time;

use crate::communication::http_request::http_request::{send_data};
use crate::communication::logging::logging::{log, LogChannel};
use crate::communication::redis::redis::{initialize_redis, RedisHandler};
use crate::sara::ble_weather_station::ble_weather_station::{connect_peripheral_device, get_data_ble};

mod sara;
mod communication;
mod tests;

type Error = String;
type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug, Serialize)]
pub struct SensorData {
    timestamp: String,
    temperature: f32,
    humidity: f32,
    wind_speed: f32,
    wind_direction: f32,
    rain: f32,
    battery_charge: f32,
    battery_voltage: f32,
}

#[tokio::main]
async fn main() {
    println!("Starting ADA");
    // 10 Minuten
    let mut interval = time::interval(Duration::from_secs(10 * 60));

    let redis_handler = match initialize_redis("redis://localhost:6379/0").await {
        Ok(handler) => Some(handler),
        Err(error) => {
            eprintln!("Failed to initialize Redis: {}", error);
            log(String::from("Error"), format!("Failed to connect to Redis: {}", error), String::from("error"));
            None
        }
    };


    if let Some(handler) = &redis_handler {
        // Wartet in anderem Task auf Nachrichten vom subscribten Channel
        let listen_handler = handler.clone();
        tokio::spawn(async move {
            if let Err(e) = listen_handler.listen().await {
                eprintln!("Error in Redis listener: {}", e);
            }
        });

        loop {
            // main loop läuft alle 10 Minuten
            interval.tick().await;

            #[cfg(not(feature = "mock"))]
            let sensor_data = match handle_sensor_data(handler).await {
                Ok(sensor_data) => Some(sensor_data),
                Err(error) => {
                    let error_log = log(String::from("Error"), error, String::from("error"));
                    let sara_log = log(String::from("Error"), String::from("Issue occurred while trying to connect to ADA"), String::from("error"));
                    handler.log_to_channel(LogChannel::Ada, error_log).await;
                    handler.log_to_channel(LogChannel::Sara, sara_log).await;
                    None
                }
            };

            #[cfg(feature = "mock")]
            let sensor_data = Some(SensorData {
                timestamp: get_time(),
                temperature: 20.0,
                humidity: 50.0,
                wind_speed: 5.0,
                wind_direction: 180.0,
                rain: 0.0,
                battery_charge: 90.0,
                battery_voltage: 3.7,
            });

            // Wenn Sensordaten vorhanden sind, werden diese an API gesendet und Logs erstellt
            if let Some(data) = sensor_data {
                match send_data("https://blickbox.maytastix.de/api/iot/api/insert", &data).await {
                    Ok(logs) => {
                        for log in logs {
                            handler.log_to_channel(LogChannel::Ada, log).await;
                        }
                    }
                    Err(error) => {
                        let error_log = log(String::from("Error"), error, String::from("error"));
                        handler.log_to_channel(LogChannel::Ada, error_log).await;
                    }
                }
            }

            // Sendet alle Logs
            if let Err(error) = handler.publish_all().await {
                eprintln!("Failed to publish logs: {}", error);
                let error_log = log(String::from("Error"), format!("Failed to publish logs: {}", error), String::from("error"));
                handler.log_to_channel(LogChannel::Ada, error_log).await;
            }
        }
    }
}

// Verarbeitet Sensordaten (Datei erstellen und Daten später hineinschreiben, Struct erstellen, zu Sara verbinden und Daten erhalten)
async fn handle_sensor_data(handler: &RedisHandler) -> Result<SensorData> {

    // Öffnet Datei in "append-mode" und erstellt sie, wenn sie nicht existiert
    let file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("command_history.txt").unwrap();

    let time = get_time();

    let mut sensor_data = SensorData {
        timestamp: time,
        temperature: 0.0,
        humidity: 0.0,
        wind_speed: 0.0,
        wind_direction: 0.0,
        rain: 0.0,
        battery_charge: 0.0,
        battery_voltage: 0.0,
    };

    // Verbindung zu Sara aufbauen
    let peripheral = connect_peripheral_device().await?;
    let ada_connected_log = log(String::from("ADA-SARA"), String::from("ADA connected successfully to SARA"), String::from("success"));
    let sara_connected_log = log(String::from("ADA-SARA"), String::from("SARA connected successfully to ADA"), String::from("success"));
    handler.log_to_channel(LogChannel::Ada, ada_connected_log).await;
    handler.log_to_channel(LogChannel::Sara, sara_connected_log).await;

    // Daten von Sara bekommen
    get_data_ble(peripheral.clone(), &mut sensor_data).await?;
    let ada_data_log = log(String::from("Sensor Data"), String::from("ADA successfully got sensor data form SARA"), String::from("success"));
    let sara_data_log = log(String::from("Sensor Data"), String::from("SARA successfully sent sensor data to ADA"), String::from("success"));
    handler.log_to_channel(LogChannel::Ada, ada_data_log).await;
    handler.log_to_channel(LogChannel::Sara, sara_data_log).await;

    // Verbindung zu Sara schließen
    peripheral.disconnect()
        .await
        .map_err(|_| String::from("Failed to disconnect from peripheral"))?;
    let successful_disconnect = log(String::from("ADA-SARA"), String::from("ADA successfully disconnected from SARA"), String::from("success"));
    handler.log_to_channel(LogChannel::Ada, successful_disconnect.clone()).await;
    handler.log_to_channel(LogChannel::Sara, successful_disconnect).await;

    write_to_file(&file, &sensor_data);

    Ok(sensor_data)
}

// Aktuelle Zeit als String, um sie API zu senden
pub fn get_time() -> String {
    let date_time_format: DateTime<Utc> = SystemTime::now().into();
    date_time_format.with_timezone(&Berlin).format("%Y-%m-%d %H:%M:%S").to_string()
}
pub fn write_to_file(mut file: &File, sensor_data: &SensorData) {
        // Schreibt erhaltene Daten in Datei auf dem Pi
        let data = format!("{:?}\n", sensor_data);
        file.write_all(data.as_bytes()).unwrap();
}

