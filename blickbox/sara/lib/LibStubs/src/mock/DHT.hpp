#ifndef DHT_MOCK_HPP
#define DHT_MOCK_HPP

#include <types/Numbers.h>
#include <iostream>

class DHT {
public:
    DHT(uint8_t pin, uint8_t type, uint8_t count = 6) 
        : _pin(pin), _type(type), _lastresult(false), pullTime(55) {
        std::cout << "DHT initialized with pin: " << (int)pin << ", type: " << (int)type << ", count: " << (int)count << std::endl;
    }

    void begin(uint8_t usec = 55) {
        std::cout << "DHT begin with usec: " << (int)usec << std::endl;
    }

    float readTemperature(bool S = false, bool force = false) {
        std::cout << "readTemperature called with S: " << S << ", force: " << force << std::endl;
        return 25.0;  // Dummy value
    }

    float convertCtoF(float celsius) {
        std::cout << "convertCtoF called with celsius: " << celsius << std::endl;
        return celsius * 9.0 / 5.0 + 32.0;  // Dummy conversion
    }

    float convertFtoC(float fahrenheit) {
        std::cout << "convertFtoC called with fahrenheit: " << fahrenheit << std::endl;
        return (fahrenheit - 32.0) * 5.0 / 9.0;  // Dummy conversion
    }

    float computeHeatIndex(bool isFahrenheit = true) {
        std::cout << "computeHeatIndex called with isFahrenheit: " << isFahrenheit << std::endl;
        return isFahrenheit ? 77.0 : 25.0;  // Dummy value
    }

    float computeHeatIndex(float temperature, float percentHumidity, bool isFahrenheit = true) {
        std::cout << "computeHeatIndex called with temperature: " << temperature << ", percentHumidity: " << percentHumidity << ", isFahrenheit: " << isFahrenheit << std::endl;
        return isFahrenheit ? 77.0 : 25.0;  // Dummy value
    }

    float readHumidity(bool force = false) {
        std::cout << "readHumidity called with force: " << force << std::endl;
        return 50.0;  // Dummy value
    }

    bool read(bool force = false) {
        std::cout << "read called with force: " << force << std::endl;
        return true;  // Dummy result
    }

private:
    uint8_t data[5];
    uint8_t _pin, _type;
    uint32_t _lastreadtime, _maxcycles;
    bool _lastresult;
    uint8_t pullTime;

    uint32_t expectPulse(bool level) {
        std::cout << "expectPulse called with level: " << level << std::endl;
        return 1000;  // Dummy value
    }
};

#endif // DHT_MOCK_HPP
