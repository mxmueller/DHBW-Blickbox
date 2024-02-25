mod sensor_modules;
mod communication;

use std::fs::{File, OpenOptions};
use std::io;

use std::io::{Read, Write};
use std::str::FromStr;
use std::time::{Duration, SystemTime};
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use serialport::SerialPort;
use tokio::time;
use crate::communication::http_request::http_request::send_data;
use crate::sensor_modules::dht_temp_hum::dht_sensor::get_dht_data;

type Error = String;
type Result<T> = std::result::Result<T, Error>;

#[derive(Clone, Debug)]
pub struct SensorData {
    timestamp: String,
    temperature: f32,
    humidity: f32,
    // wind_speed: String,
    // wind_direction: String,
    // precipitation_amount: String,
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

    // seeing available ports in terminal
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }

    let mut port: Box<dyn SerialPort> = serialport::new("/dev/ttyACM0", 115200)
        .timeout(Duration::from_millis(3000))
        .open()
        .map_err(|error| format!("Failed to open port: {:?}", error))?;

    // Timer interval for sending commands (every 30 minutes)
    let mut interval = time::interval(Duration::from_secs(30 * 60));

    let time = get_time();

    let mut sensor_data = SensorData {
        timestamp: time,
        temperature: 0.0,
        humidity: 0.0,
        // wind_speed: String::new(),
        // wind_direction: String::new(),
        // precipitation_amount: String::new(),
    };

    // here the programm is waiting for an initial message before further data is requested
    let mut serial_buf: Vec<u8> = vec![0; 100];
    let mut initial_message_received = false;
    let mut initial_message = String::new();

    while initial_message_received == false {
        match port.read(serial_buf.as_mut_slice()) {
            Ok(t) => {
                let received_data = &serial_buf[..t];
                let string = String::from_utf8_lossy(received_data).to_string();
                initial_message += string.as_str();
                initial_message_received = check_for_initial_message(initial_message.clone());
            }
            Err(ref e) if e.kind() == io::ErrorKind::TimedOut => {
                serial_buf.clear();
                Err(format!("Timeout occured while trying to get the initial message. {:?}", e))?
            }
            Err(e) => {
                serial_buf.clear();
                Err(format!("Failed to read from port: {}", e))?
            }
        }
    }

    // the main loop to get data every 30 minutes
    loop {
        interval.tick().await;

        let mut port = port.try_clone().map_err(|error| format!("{:?}", error))?;

        let temperature = get_dht_data("t\n", &mut port).await?;
        println!("send t command, got: {}", temperature);
        let humidity = get_dht_data("h\n", &mut port).await?;
        println!("send h command, got: {}", humidity);

        sensor_data.temperature = f32::from_str(&*temperature).unwrap();
        sensor_data.humidity = f32::from_str(&*humidity).unwrap();

        write_to_file(&file, &sensor_data);
        // handle_weather_station_data();

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

pub fn check_for_initial_message(initial_message: String) -> bool {
    let is_message_received;

    match initial_message.as_str() {
        "Ello Sara here :D\r\nI am initialized!\r\nCommands: t - temp, h - humidity\r\n" => {
            println!("yay, the port is initialized");
            is_message_received = true;
        }
        _ => {
            is_message_received = false;
        }
    }

    return is_message_received
}

pub fn interpret_data(data: &[u8]) -> String {
    /// no error handling lol, no risk no fun
    // here i am interpreting the received string before returning it :)
    // : als Seperator zwischen Key und Value der Werte und String wird mit \n beendet und weitere cases werden abgedeckt
    let mut  string = String::from_utf8_lossy(data).to_string();

    println!("received data to be interpreted: {:?}", string);

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
        return separated_string_by_colon[1].to_string()
    } else if separated_string_by_colon.len() > 2 {
        println!("Interpreted data: {:?}", separated_string_by_colon[separated_string_by_colon.len() - 1 ].to_string());
        return separated_string_by_colon[separated_string_by_colon.len() - 1 ].to_string()
    } else {
        // no clue what the received data could be in this case
        println!("damn, didnt work");
        return String::new()
    }
}