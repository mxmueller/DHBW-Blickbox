pub mod mocking_sensor_data {
    use rand::Rng;

    use crate::SensorData;

    pub fn generate_mock_sensor_data() -> SensorData {
        let mut rng = rand::thread_rng();
        SensorData {
            timestamp: chrono::Utc::now().to_rfc3339(),
            temperature: rng.gen_range(-10.0..40.0),
            humidity: rng.gen_range(0.0..100.0),
            wind_speed: rng.gen_range(0.0..100.0),
            wind_direction: rng.gen_range(0.0..360.0),
            rain: rng.gen_range(0.0..50.0),
            battery_charge: rng.gen_range(0.0..100.0),
            battery_voltage: rng.gen_range(3.0..4.2),
        }
    }

}