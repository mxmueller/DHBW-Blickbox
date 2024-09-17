#include <math.h>
#include <sara_battery.hpp>
#include <unity.h>

using namespace sara_battery;

enum {
BATTERY_PIN = 6
};
SaraBatteryManager battery_manager (BATTERY_PIN);


void setUp() {
}

void tearDown() {
}

void test_correct_ADC_units(){
    float units = ADC_REF_VOLTAGE / ADC_UNITS;
    TEST_ASSERT_EQUAL_FLOAT(units, 0.003222656);
}

void test_battery_calculate_voltage_from_ADC_Value() {
    uint16_t raw_battery_value = 512;
    float battery_voltage = calculate_battery_voltage(raw_battery_value);
    TEST_ASSERT_EQUAL_FLOAT(battery_voltage, 3.3);
}

void test_battery_map_voltage() {
    uint8_t voltage = 3.69;
    float battery_percent = map_to_battery_level(voltage);
    TEST_ASSERT_EQUAL_INT8(battery_percent, -5);
}

auto main( int  /*argc*/, char ** /*argv*/) -> int {
    UNITY_BEGIN();

    RUN_TEST(test_correct_ADC_units);
    RUN_TEST(test_battery_calculate_voltage_from_ADC_Value);
    RUN_TEST(test_battery_map_voltage);
    UNITY_END();
}
    