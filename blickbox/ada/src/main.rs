mod sensor_modules;

use std::{io, thread};
use std::fs::OpenOptions;

use std::io::{Read, Write};
use std::time::{Duration, SystemTime};
use chrono::{DateTime, Utc};
use chrono_tz::Europe::Berlin;
use tokio::time;

//use crate::sensor_modules;


#[tokio::main]
async fn main() {
    // Opens file in append mode (and creating it if it doesn't exist)
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .create(true)
        .open("command_history.txt").unwrap();
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }

    let mut port = serialport::new("/dev/ttyACM0", 115200)
        .timeout(Duration::from_millis(1000))
        .open().expect("Failed to open port");

    // Initial delay before sending the first command
    tokio::time::sleep(Duration::from_secs(5)).await;

    tokio::time::sleep(Duration::from_millis(5000)).await;

    let mut serial_buf: Vec<u8> = vec![0; 100];


    //handle_dht_sensor_data();

    // Timer interval for sending commands (every 30 minutes)
    let mut interval = time::interval(Duration::from_secs(120));

    loop {
        interval.tick().await;

        // here data is requested
        let temperature_command = "t\n";
        port.write_all(temperature_command.as_ref()).expect("Failed to send command");

        match port.read(serial_buf.as_mut_slice()) {
            Ok(t) => {
                let received_data = &serial_buf[..t];
                let interpreted_data = interpret_data(received_data);

                // writing the received data to file system
                // data to be written should be a struct sooner or later... :/
                if !interpreted_data.is_empty() {
                    let date_time_format: DateTime<Utc> = SystemTime::now().into();
                    let time = date_time_format.with_timezone(&Berlin).format("%Y-%m-%d %H:%M:%S").to_string();
                    let data = format!("{:?}, {:?}\n", time, interpreted_data);
                    file.write_all(data.as_bytes()).unwrap();
                }

                tokio::time::sleep(Duration::from_millis(1000)).await;
                continue;
            }
            Err(ref e) if e.kind() == io::ErrorKind::TimedOut => {
                println!("Timeout occurred");
                continue;
            }
            Err(e) => {
                eprintln!("Failed to read from port: {}", e);
                break;
            }
        };
    }

    println!("why");
    tokio::time::sleep(Duration::from_millis(8000)).await;
    print!("is is is");
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
            if separated_string_by_colon.len() >= 2 {
                println!("Interpreted data: {:?}", separated_string_by_colon[1].clone().to_string());
                separated_string_by_colon[1].clone().to_string()
            } else {
                println!("damn, didnt work");
                String::new()
            }
        }
    }
}