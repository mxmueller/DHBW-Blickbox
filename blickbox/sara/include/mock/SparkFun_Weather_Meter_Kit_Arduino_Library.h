#ifndef __SPARKFUN_WEATHER_METER_KIT_H__
#define __SPARKFUN_WEATHER_METER_KIT_H__

#include <types/Numbers.h>
#include <stubs/ArduinoStubs.hpp>
#include <makros/ArdunioMakros.hpp>
#include <math.h>

// Enum to define the indexes for each wind direction
enum SFEWeatherMeterKitAnemometerAngles
{
    WMK_ANGLE_0_0 = 0,
    WMK_ANGLE_22_5,
    WMK_ANGLE_45_0,
    WMK_ANGLE_67_5,
    WMK_ANGLE_90_0,
    WMK_ANGLE_112_5,
    WMK_ANGLE_135_0,
    WMK_ANGLE_157_5,
    WMK_ANGLE_180_0,
    WMK_ANGLE_202_5,
    WMK_ANGLE_225_0,
    WMK_ANGLE_247_5,
    WMK_ANGLE_270_0,
    WMK_ANGLE_292_5,
    WMK_ANGLE_315_0,
    WMK_ANGLE_337_5,
    WMK_NUM_ANGLES
};

// Angle per index of wind vane (360 / 16 = 22.5)
#define SFE_WIND_VANE_DEGREES_PER_INDEX (360.0 / WMK_NUM_ANGLES)

// The ADC of each platform behaves slightly differently. Some have different
// resolutions, some have non-linear outputs, and some voltage divider circuits
// are different. The expected ADV values have been obtained experimentally for
// various platforms below
#ifdef AVR
    // Tested with RedBoard Qwiic with Weather Shield
    #define SFE_WMK_ADC_ANGLE_0_0 902
    #define SFE_WMK_ADC_ANGLE_22_5 661
    #define SFE_WMK_ADC_ANGLE_45_0 701
    #define SFE_WMK_ADC_ANGLE_67_5 389
    #define SFE_WMK_ADC_ANGLE_90_0 398
    #define SFE_WMK_ADC_ANGLE_112_5 371
    #define SFE_WMK_ADC_ANGLE_135_0 483
    #define SFE_WMK_ADC_ANGLE_157_5 430
    #define SFE_WMK_ADC_ANGLE_180_0 570
    #define SFE_WMK_ADC_ANGLE_202_5 535
    #define SFE_WMK_ADC_ANGLE_225_0 812
    #define SFE_WMK_ADC_ANGLE_247_5 792
    #define SFE_WMK_ADC_ANGLE_270_0 986
    #define SFE_WMK_ADC_ANGLE_292_5 925
    #define SFE_WMK_ADC_ANGLE_315_0 957
    #define SFE_WMK_ADC_ANGLE_337_5 855

    #define SFE_WMK_ADC_RESOLUTION 10
#elif ESP32
    // Tested with ESP32 processor board installed on Weather Carrier
    #define SFE_WMK_ADC_ANGLE_0_0 3118
    #define SFE_WMK_ADC_ANGLE_22_5 1526
    #define SFE_WMK_ADC_ANGLE_45_0 1761
    #define SFE_WMK_ADC_ANGLE_67_5 199
    #define SFE_WMK_ADC_ANGLE_90_0 237
    #define SFE_WMK_ADC_ANGLE_112_5 123
    #define SFE_WMK_ADC_ANGLE_135_0 613
    #define SFE_WMK_ADC_ANGLE_157_5 371
    #define SFE_WMK_ADC_ANGLE_180_0 1040
    #define SFE_WMK_ADC_ANGLE_202_5 859
    #define SFE_WMK_ADC_ANGLE_225_0 2451
    #define SFE_WMK_ADC_ANGLE_247_5 2329
    #define SFE_WMK_ADC_ANGLE_270_0 3984
    #define SFE_WMK_ADC_ANGLE_292_5 3290
    #define SFE_WMK_ADC_ANGLE_315_0 3616
    #define SFE_WMK_ADC_ANGLE_337_5 2755

    #define SFE_WMK_ADC_RESOLUTION 12
#else
    // Values calculated assuming 10k pullup and perfectly linear 16-bit ADC
    #define SFE_WMK_ADC_ANGLE_0_0 50294
    #define SFE_WMK_ADC_ANGLE_22_5 25985
    #define SFE_WMK_ADC_ANGLE_45_0 29527
    #define SFE_WMK_ADC_ANGLE_67_5 5361
    #define SFE_WMK_ADC_ANGLE_90_0 5958
    #define SFE_WMK_ADC_ANGLE_112_5 4219
    #define SFE_WMK_ADC_ANGLE_135_0 11818
    #define SFE_WMK_ADC_ANGLE_157_5 8099
    #define SFE_WMK_ADC_ANGLE_180_0 18388
    #define SFE_WMK_ADC_ANGLE_202_5 15661
    #define SFE_WMK_ADC_ANGLE_225_0 40329
    #define SFE_WMK_ADC_ANGLE_247_5 38365
    #define SFE_WMK_ADC_ANGLE_270_0 60494
    #define SFE_WMK_ADC_ANGLE_292_5 52961
    #define SFE_WMK_ADC_ANGLE_315_0 56785
    #define SFE_WMK_ADC_ANGLE_337_5 44978

    #define SFE_WMK_ADC_RESOLUTION 16

    // Set macro to indicate that this platform isn't known
    #define SFE_WMK_PLAFTORM_UNKNOWN
#endif

// Calibration parameters for each sensor
struct SFEWeatherMeterKitCalibrationParams
{
    // Wind vane
    uint16_t vaneADCValues[WMK_NUM_ANGLES];

    // Wind speed
    uint32_t windSpeedMeasurementPeriodMillis;
    float kphPerCountPerSec;

    // Rainfall
    float mmPerRainfallCount;
    uint32_t minMillisPerRainfall;
};

class SFEWeatherMeterKit
{
  public:
    // Constructor
    SFEWeatherMeterKit(uint8_t windDirectionPin, uint8_t windSpeedPin, uint8_t rainfallPin);
    static void begin();

    // Data collection
    static float getWindDirection();
    static float getWindSpeed();
    static float getTotalRainfall();

    // Sensor calibration params
    static SFEWeatherMeterKitCalibrationParams getCalibrationParams();
    static void setCalibrationParams(SFEWeatherMeterKitCalibrationParams params);

    // ADC resolution scaling
    static void setADCResolutionBits(uint8_t resolutionBits);

    // Helper functions. These can be helpful for sensor calibration
    static uint32_t getWindSpeedCounts();
    static uint32_t getRainfallCounts();
    static void resetWindSpeedFilter();
    static void resetTotalRainfall();

  private:
    // Updates wind speed
    static void updateWindSpeed();

    // Interrupt handlers
    static void windSpeedInterrupt();
    static void rainfallInterrupt();

    // Pins for each sensor
    static uint8_t _windDirectionPin;
    static uint8_t _windSpeedPin;
    static uint8_t _rainfallPin;

    // Sensor calibration parameters
    static SFEWeatherMeterKitCalibrationParams _calibrationParams;

    // Variables to track measurements
    static uint32_t _windCounts;
    static uint32_t _windCountsPrevious;
    static uint32_t _rainfallCounts;
    static uint32_t _lastWindSpeedMillis;
    static uint32_t _lastRainfallMillis;
};

#endif