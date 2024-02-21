pub mod dht_sensor {
    use std::io;
    use std::time::Duration;
    use serialport::SerialPort;
    use crate::interpret_data;

    pub async fn get_dht_data(command: &str, mut port: &mut Box<dyn SerialPort>) -> crate::Result<String> {

        let mut serial_buf: Vec<u8> = vec![0; 100];

        // here data is requested
        if command == "h\n" || command == "t\n" {
            port.write_all(command.as_ref()).expect("Failed to send command");
        }
        tokio::time::sleep(Duration::from_millis(1000)).await;

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
}