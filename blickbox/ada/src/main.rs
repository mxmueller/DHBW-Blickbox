mod sensor_modules;

use std::{io, thread};
use std::fs::{File, OpenOptions};

use std::io::{Read, Write};
use std::time::{Duration, SystemTime};
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use serialport::SerialPort;
use tokio::time;
use crate::sensor_modules::dht_temp_hum::dht_sensor::get_dht_data;

type Error = String;
type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug)]
pub struct SensorData {
    timestamp: String,
    temperature: String,
    humidity: String,
    wind_direction: i32,
    wind_speed: f32,
    precipitation_amount: f32,
}

#[tokio::main]
async fn main() {

    if let Err(error) = execute().await {
        // here it should send the error to the cloud for it to be noted or fixed
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

    // seeing available ports in terminal
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }

    let mut port: Box<dyn SerialPort> = serialport::new("/dev/ttyACM0", 115200)
        .timeout(Duration::from_millis(1000))
        .open()
        .map_err(|error| format!("Failed to open port: {:?}", error))?;

    // Initial delay before sending the first command
    tokio::time::sleep(Duration::from_secs(5)).await;

    tokio::time::sleep(Duration::from_millis(5000)).await;

    // Timer interval for sending commands (every 30 minutes)
    let mut interval = time::interval(Duration::from_secs(20));

    let time = get_time();

    let mut sensor_data = SensorData {
        timestamp: time,
        temperature: String::new(),
        humidity: String::new(),
        wind_direction: 0,
        wind_speed: 0.0,
        precipitation_amount: 0.0,
    };

    loop {
        interval.tick().await;

        let mut port = port.try_clone().map_err(|error| format!("{:?}", error))?;

        let temperature = get_dht_data("t\n", &mut port).await?;
        let humidity = get_dht_data("h\n", &mut port).await?;

        sensor_data.temperature = temperature;
        sensor_data.humidity = humidity;

        write_to_file(&file, &sensor_data);

        // handle_weather_station_data();
    }
}

pub fn get_time() -> String {
    let date_time_format: DateTime<Utc> = SystemTime::now().into();
    let time = date_time_format.with_timezone(&Berlin).format("%Y-%m-%d %H:%M:%S").to_string();
    return time;
}
pub fn write_to_file(mut file: &File, sensor_data: &SensorData) {
    // writing the received data to file system
    // data to be written should be a struct sooner or later... :/
        let data = format!("{:?}\n", sensor_data);
        file.write_all(data.as_bytes()).unwrap();
}

pub fn interpret_data(data: &[u8]) -> String {
    /// no error handling lol, no risk no fun
    // here i am interpreting the received string before storing it into the buffer :)
    // : als Seperator zwischen Key und Value der Werte und String wird mit \n beendet
    // println!(" data: {:?}", data);
    let mut  string = String::from_utf8_lossy(data).to_string();

    println!("received data to be interpreted: {:?}", string);

    return match string.as_str() {
        "Ello Sara here :D\r\nI am initialized!\r\nCommands: t - temp, h - humidity\r\n" => {
            String::new()
        }
        _ => {
            // Remove trailing \r\n or \n characters
            if string.ends_with("\n") {
                string.pop();
            }
            if string.ends_with("\r") {
                string.pop();
            }

            let separated_string_by_colon = string.split(':').collect::<Vec<&str>>();

            // if there would be more commands in the received_data
            // ...I'm not sure it would catch the correct data as interpreted_data everytime
            if separated_string_by_colon.len() == 2 {
                println!("Interpreted data: {:?}", separated_string_by_colon[1].to_string());
                separated_string_by_colon[1].to_string()
            } else if separated_string_by_colon.len() > 2 {
                println!("Interpreted data: {:?}", separated_string_by_colon[separated_string_by_colon.len() - 1 ].to_string());
                separated_string_by_colon[separated_string_by_colon.len() - 1 ].to_string()
            } else {
                // no clue what the received data could be in this case
                println!("damn, didnt work");
                String::new()
            }
        }
    }
}