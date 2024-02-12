use std::{io, thread};
use std::borrow::Cow;

use std::io::{Read, Write};
use std::time::Duration;

fn main() {
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }

    let mut port = serialport::new("/dev/ttyACM0", 115200)
        .timeout(Duration::from_millis(1000))
        .open().expect("Failed to open port");

    thread::sleep(Duration::from_millis(1000));


    // This is exemplary code to work with the string because nothing is received from Port
        let mock_data = b"t:60\n";
        println!("Received mock data: {:?}", mock_data);

        let interpreted_data = interpret_data(mock_data);

        println!("Interpreted mock data: {}", interpreted_data);
    // End to exemplary code

    let mut serial_buf: Vec<u8> = vec![0; 100];

    // here data is requested
    let temperature_command = b"t\r\n";
    port.write_all(temperature_command).expect("Failed to send command");


    match port.read_to_end(&mut serial_buf) {
        Ok(t) => {
            // Handling of received data
            let received_data = &serial_buf[..t];

            //let received_data = "t:60\n"; /// exemplary string bc nothing is received from port (otherwise use line above)
            println!("Received: {:?}", received_data);
            let interpreted_data = interpret_data(received_data);
            println!("Interpreted data: {}", interpreted_data);

            io::stdout().write_all(&serial_buf[..t]).expect("Failed to write buffer D:");
            thread::sleep(Duration::from_millis(1000));

            serial_buf.clear();
        }
        Err(x) => {
            println!("Whats happeninnnng?: {:?}", x);
        }
    };

}

pub fn interpret_data(data: &[u8]) -> String {
    /// no error handling lol, no risk no fun
    // here i am interpreting the received string before storing it into the buffer :)
    // : als Seperator zwischen Key und Value der Werte und String wird mit \n beendet
    println!(" data: {:?}", data);
    let mut  string = String::from_utf8_lossy(data).to_string();

    println!("received data to be interpreted: {:?}", string);
    if string.ends_with("\n") {
       string.pop();
    }

    if string.ends_with("\r") {
        string.pop();
    }

    // Remove trailing \r\n or \n characters
    //string = string.trim_end_matches('\r').trim_end_matches('\n').to_string();

    let separated_string_by_colon = string.split(':').collect::<Vec<&str>>();

    if separated_string_by_colon.len() >= 2 {
        return separated_string_by_colon[1].clone().to_string();
    } else {

        println!("damn, didnt work");
        return String::new()
    }
}