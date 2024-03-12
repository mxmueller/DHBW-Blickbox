#include <sara_battery.hpp>

namespace sara_battery{
     battery_value battery;

     void update_battery_data(){
        battery.raw_adc = analogRead(BATTERY_PIN);
        battery.level = map(battery.raw_adc, 200, 1023, 0, 100);
     }
}

