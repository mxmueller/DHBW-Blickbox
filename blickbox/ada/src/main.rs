mod sara;
mod communication;

use std::fs::{File, OpenOptions};

use std::io::{Read, Write};
use std::str::FromStr;
use std::time::{Duration, SystemTime};
use btleplug::api::Peripheral;
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use serialport::SerialPort;
use tokio::time;
use crate::communication::http_request::http_request::send_data;
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
    precipitation_amount: f32,
}

#[tokio::main]
async fn main() {

    if let Err(error) = execute().await {
        // here it should send the error to the cloud for it to be noted or fixed
        // should that be handled in the execute() bc its gotta be send as a log with a log-flag...
        eprintln!("{}", error);
    }
}

async fn execute() -> Result<()> {

    // Opens file in append mode (and creating it if it doesn't exist)
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .create(true)
        .open("command_history.txt").unwrap();

    // Timer interval for sending commands (every 30 minutes)
    let mut interval = time::interval(Duration::from_secs(30 * 60));

    let time = get_time();

    let mut sensor_data = SensorData {
        timestamp: time,
        temperature: 0.0,
        humidity: 0.0,
        wind_speed: 0.0,
        wind_direction: 0.0,
        precipitation_amount: 0.0,
    };

    // the main loop to get data every 30 minutes
    loop {
        interval.tick().await;

        let peripheral = connect_peripheral_device().await?;
        get_data_ble(peripheral.clone(), &mut sensor_data).await?;
        // Disconnect from the peripheral
        peripheral.disconnect()
            .await
            .map_err(|_| String::from("Failed to disconnect from peripheral"))?;

        write_to_file(&file, &sensor_data);

        send_data(&sensor_data).await?;
    }
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
