pub mod weather_station {
    use std::io;
    use std::time::Duration;
    use serialport::SerialPort;

    pub async fn get_weather_station_data(command: &str, mut port: &mut Box<dyn SerialPort>) -> crate::Result<String> {

        let mut serial_buf: Vec<u8> = vec![0; 100];

        // here data is requested
        if command == "h\n" || command == "t\n" || command == "ws\n" || command == "wd\n" || command == "rfm\n" {
            port.write_all(command.as_ref()).expect("Failed to send command");
        }
        tokio::time::sleep(Duration::from_millis(5000)).await;

        match port.read(serial_buf.as_mut_slice()) {
            Ok(t) => {
                let received_data = &serial_buf[..t];
                let interpreted_data = interpret_data(received_data);
                serial_buf.clear();
                Ok(interpreted_data)
            }
            Err(ref e) if e.kind() == io::ErrorKind::TimedOut => {
                serial_buf.clear();
                Err(format!("Timeout occured. {:?}", e))
            }
            Err(e) => {
                serial_buf.clear();
                Err(format!("Failed to read from port: {}", e))
            }
        }
    }

    pub fn interpret_data(data: &[u8]) -> String {
        /// no error handling lol, no risk no fun
        // here i am interpreting the received string before returning it :)
        // : als Seperator zwischen Key und Value der Werte und String wird mit \n beendet und weitere cases werden abgedeckt
        let mut string = String::from_utf8_lossy(data).to_string();

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
            println!("Interpreted data: {:?}", separated_string_by_colon[separated_string_by_colon.len() - 1].to_string());
            return separated_string_by_colon[separated_string_by_colon.len() - 1].to_string()
        } else {
            // no clue what the received data could be in this case
            println!("damn, didnt work");
            return String::new()
        }
    }
}