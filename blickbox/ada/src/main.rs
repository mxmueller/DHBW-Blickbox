mod sara;
mod communication;

use std::collections::VecDeque;
use std::fs::{File, OpenOptions};
use std::io;

use std::io::{Read, Write};
use std::str::FromStr;
use std::time::{Duration, SystemTime};
use btleplug::api::Peripheral;
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use serialport::SerialPort;
use tokio::time;
use crate::communication::http_request::http_request::{send_data, send_last_online};
use crate::communication::logging::http_request::{log, LogEntry, send_logs};
use crate::sara::ble_weather_station::ble_weather_station::{connect_peripheral_device, get_data_ble};
use crate::sara::weather_station::weather_station::get_weather_station_data;

type Error = String;
type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug)]
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

    let mut ringbuffer: VecDeque<LogEntry> = VecDeque::new();

    // Timer interval for sending commands (every 10 minutes)
    let mut interval = time::interval(Duration::from_secs(10 * 60));

    loop {
        // the main loop to get data every 30 minutes
        interval.tick().await;

        if let Err(error) = handle_sensor_data(&mut ringbuffer).await {
            // here it should send the error to the cloud for it to be noted or fixed
            // should that be handled in the execute() bc its gotta be send as a log with a log-flag...
            eprintln!("{}", error);
            log(String::from("Error"), format!("{}", error), String::from("error"), &mut ringbuffer);
        }
        if let Err(error) = send_last_online().await {
            eprintln!("{}", error);
            log(String::from("Error"), format!("{}", error), String::from("error"), &mut ringbuffer);
        }
        send_logs(&mut ringbuffer).await.expect("Failed to send log");
    }
}

async fn handle_sensor_data(ringbuffer: &mut VecDeque<LogEntry>) -> Result<()> {

    // Opens file in append mode (and creating it if it doesn't exist)
    let mut file = OpenOptions::new()
        .write(true)
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

    let peripheral = connect_peripheral_device().await?;
    log(String::from("Info"), String::from("ADA connected successfully to SARA"), String::from("success"), ringbuffer);
    get_data_ble(peripheral.clone(), &mut sensor_data).await?;
    log(String::from("Info"), String::from("ADA successfully got sensor data form SARA"), String::from("success"), ringbuffer);
    // Disconnect from the peripheral
    peripheral.disconnect()
        .await
        .map_err(|_| String::from("Failed to disconnect from peripheral"))?;


    write_to_file(&file, &sensor_data);

    send_data(&sensor_data).await?;

    Ok(())
}

pub fn get_time() -> String {
    let date_time_format: DateTime<Utc> = SystemTime::now().into();
    let time = date_time_format.with_timezone(&Berlin).format("%Y-%m-%d %H:%M:%S").to_string();
    return time;
}
pub fn write_to_file(mut file: &File, sensor_data: &SensorData) {
        // writing the received data to file system
        let data = format!("{:?}\n", sensor_data);
        file.write_all(data.as_bytes()).unwrap();
}
