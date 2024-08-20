import pytest
import requests
from unittest.mock import Mock
import os
from dotenv import load_dotenv
load_dotenv()

use_dev_container = os.getenv("API_USE_DEV_CONTAINER", "false").lower() == "true"

def getURL(path):
    if(use_dev_container):
        return "http://localhost:5000/iot/api" + path
    else:
        return "http://dhbwapi.maytastix.de/iot/api" + path


session = requests.Session()
session.headers.update({"blickbox": "true"})

@pytest.mark.usefixtures("skip_ping_tests")
def test_db_status(skip_ping_tests):
    if skip_ping_tests:
        pytest.skip("No-Ping Option gesetzt")
    response = session.get(getURL("/pingDB"))
    assert response.status_code == 200
    expected_data = {'message': 'Verbindung zur Datenbank steht'}
    assert response.json() == expected_data

# Test ob der Grafana Server läuft
@pytest.mark.usefixtures("skip_ping_tests")
def test_grafana_status(skip_ping_tests):
    if skip_ping_tests:
        pytest.skip("No-Ping Option gesetzt")
    response = session.get(getURL("/pingGF"))
    assert response.status_code == 200
    expected_data = {'message': 'Verbindung zu Grafana steht'}
    assert response.json() == expected_data

##########################################################################
# Temperatur Unit-Tests

@pytest.mark.usefixtures("skip_temp_tests")
@pytest.mark.parametrize("temperature", [-60.1, -490348204903.3])
def test_temperature_edge_cases_negative(skip_temp_tests, temperature):
    if skip_temp_tests:
        pytest.skip("No-Temp Option gesetzt")
    payload = {"temperature": temperature}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Temperatur nicht in Range"}

@pytest.mark.usefixtures("skip_temp_tests")
@pytest.mark.parametrize("temperature", [100.1, 44343532.1])
def test_temperature_edge_cases_positive(skip_temp_tests, temperature):
    if skip_temp_tests:
        pytest.skip("No-Temp Option gesetzt")
    payload = {"temperature": temperature}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Temperatur nicht in Range"}

@pytest.mark.usefixtures("skip_temp_tests")
def test_temperature_edge_cases_string(skip_temp_tests):
    if skip_temp_tests:
        pytest.skip("No-Temp Option gesetzt")
    payload = {"temperature": "hello"}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 500

@pytest.mark.usefixtures("skip_temp_tests")
def test_temperature_wrong_key(skip_temp_tests):
    if skip_temp_tests:
        pytest.skip("No-Temp Option gesetzt")
    payload = {"air-humidity": 18.1}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_temp_tests")
def test_temperature_wrong_timestamp(skip_temp_tests):
    if skip_temp_tests:
        pytest.skip("No-Temp Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "temperature": 18.1}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}

# ##########################################################################
# # Luftfeuchtigkeits Unit-Tests

@pytest.mark.usefixtures("skip_humid_tests")
@pytest.mark.parametrize("humidity", [-0.1, -100])
def test_airhumidity_edge_cases_negative(skip_humid_tests,humidity):
    if skip_humid_tests:
        pytest.skip("No-Humid Option gesetzt")
    payload = {"air_humidity": humidity}
    response = session.post(getURL("/insert/air-humidity"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}

@pytest.mark.usefixtures("skip_humid_tests")
@pytest.mark.parametrize("humidity", [100.1, 44343532.1])
def test_airhumidity_edge_cases_positive(skip_humid_tests, humidity):
    if skip_humid_tests:
        pytest.skip("No-Humid Option gesetzt")
    payload = {"air_humidity": humidity}
    response = session.post(getURL("/insert/air-humidity"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}

@pytest.mark.usefixtures("skip_humid_tests")
def test_airhumidity_edge_cases_string(skip_humid_tests):
    if skip_humid_tests:
        pytest.skip("No-Humid Option gesetzt")
    payload = {"air_humidity": "hello"}
    response = session.post(getURL("/insert/air-humidity"), json=payload)
    assert response.status_code == 500

@pytest.mark.usefixtures("skip_humid_tests")
def test_airhumidity_wrong_key(skip_humid_tests):
    if skip_humid_tests:
        pytest.skip("No-Humid Option gesetzt")
    payload = {"temperature": 18.1}
    response = session.post(getURL("/insert/air-humidity"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_humid_tests")
def test_airhumidity_wrong_timestamp(skip_humid_tests):
    if skip_humid_tests:
        pytest.skip("No-Humid Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "air_humidityy": 18.1}
    response = session.post(getURL("/insert/air-humidity"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}

# ##########################################################################
# # Windgeschwindigkeits Unit-Tests

@pytest.mark.usefixtures("skip_windspeed_tests")
@pytest.mark.parametrize("wind_speed", [-0.1, -1000])
def test_wind_speed_edge_cases_negative(skip_windspeed_tests, wind_speed):
    if skip_windspeed_tests:
        pytest.skip("No-Wind-Speed Option gesetzt")
    payload = {"wind_speed": wind_speed}
    response = session.post(getURL("/insert/wind-speed"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}

@pytest.mark.usefixtures("skip_windspeed_tests")
@pytest.mark.parametrize("wind_speed", [500.1, 44343532.1])
def test_wind_speed_edge_cases_positive(skip_windspeed_tests, wind_speed):
    if skip_windspeed_tests:
        pytest.skip("No-Wind-Speed Option gesetzt")
    payload = {"wind_speed": wind_speed}
    response = session.post(getURL("/insert/wind-speed"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}

@pytest.mark.usefixtures("skip_windspeed_tests")
def test_wind_speed_edge_cases_string(skip_windspeed_tests):
    if skip_windspeed_tests:
        pytest.skip("No-Wind-Speed Option gesetzt")
    payload = {"wind_speed": "hello"}
    response = session.post(getURL("/insert/wind-speed"), json=payload)
    assert response.status_code == 500

@pytest.mark.usefixtures("skip_windspeed_tests")
def test_wind_speed_wrong_key(skip_windspeed_tests):
    if skip_windspeed_tests:
        pytest.skip("No-Wind-Speed Option gesetzt")
    payload = {"hallo": 50}
    response = session.post(getURL("/insert/wind-speed"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_windspeed_tests")
def test_wind_speed_wrong_timestamp(skip_windspeed_tests):
    if skip_windspeed_tests:
        pytest.skip("No-Wind-Speed Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "wind-speed": 18.1}
    response = session.post(getURL("/insert/wind-speed"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}


################################################################
# Windrichtungs Unit-Tests

@pytest.mark.usefixtures("skip_winddir_tests")
@pytest.mark.parametrize("wind_direction", [-60.1, -490348204903.3, -0.1])
def test_wind_direction_edge_cases_negative(skip_winddir_tests, wind_direction):
    if skip_winddir_tests:
        pytest.skip("No-WindDir Option gesetzt")
    payload = {"wind_direction": wind_direction}
    response = session.post(getURL("/insert/wind-direction"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Windrichtungs Wert nicht in Range"}


@pytest.mark.usefixtures("skip_winddir_tests")
@pytest.mark.parametrize("wind_direction", [360.1, 490348204903.3, 4002.])
def test_wind_direction_edge_cases_positive(skip_winddir_tests, wind_direction):
    if skip_winddir_tests:
        pytest.skip("No-WindDir Option gesetzt")
    payload = {"wind_direction": wind_direction}
    response = session.post(getURL("/insert/wind-direction"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Windrichtungs Wert nicht in Range"}



@pytest.mark.usefixtures("skip_winddir_tests")
def test_wind_direction_edge_case_string(skip_winddir_tests):
    if skip_winddir_tests:
        pytest.skip("No-WindDir Option gesetzt")
    payload = {"wind_direction": "hello"}
    response = session.post(getURL("/insert/wind-direction"), json=payload)
    assert response.status_code == 500



@pytest.mark.usefixtures("skip_winddir_tests")
def test_wind_direction_edge_case_wrong_key(skip_winddir_tests):
    if skip_winddir_tests:
        pytest.skip("No-WindDir Option gesetzt")
    payload = {"hello": 344.3}
    response = session.post(getURL("/insert/wind-direction"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}


@pytest.mark.usefixtures("skip_winddir_tests")
def test_wind_direction_edge_case_wrong_timestamp(skip_winddir_tests):
    if skip_winddir_tests:
        pytest.skip("No-WindDir Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "wind_direction": 18.1}
    response = session.post(getURL("/insert/wind-direction"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}


################################################################################################
# Niederschlags-Route Test


@pytest.mark.usefixtures("skip_rain_tests")
@pytest.mark.parametrize("rain", [-60.1, -490348204903.3, -0.1])
def test_rain_edge_cases_negative(skip_rain_tests, rain):
    if skip_rain_tests:
        pytest.skip("No-Rain Option gesetzt")
    payload = {"rain": rain}
    response = session.post(getURL("/insert/rain"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Niederschlag nicht in Range"}

@pytest.mark.usefixtures("skip_rain_tests")
@pytest.mark.parametrize("rain", [1100.1, 490348204903.3, 5434])
def test_rain_edge_cases_positve(skip_rain_tests, rain):
    if skip_rain_tests:
        pytest.skip("No-Rain Option gesetzt")
    payload = {"rain": rain}
    response = session.post(getURL("/insert/rain"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Niederschlag nicht in Range"}



@pytest.mark.usefixtures("skip_rain_tests")
def test_rain_edge_case_string(skip_rain_tests):
    if skip_rain_tests:
        pytest.skip("No-Rain Option gesetzt")
    payload = {"rain": "rain"}
    response = session.post(getURL("/insert/rain"), json=payload)
    assert response.status_code == 500

@pytest.mark.usefixtures("skip_rain_tests")
def test_rain_edge_case_wrong_key(skip_rain_tests):
    if skip_rain_tests:
        pytest.skip("No-Rain Option gesetzt")
    payload = {"hello": 22}
    response = session.post(getURL("/insert/rain"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_rain_tests")
def test_rain_edge_case_wrong_timestamp(skip_rain_tests):
    if skip_rain_tests:
        pytest.skip("No-Rain Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "rain": 18.1}
    response = session.post(getURL("/insert/rain"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}

###################################################################
# Batterieladung Tests

@pytest.mark.usefixtures("skip_batteryc_tests")
@pytest.mark.parametrize("battery_charge", [-60.1, -490348204903.3, -0.1])
def test_batteryc_edge_cases_negative(skip_batteryc_tests, battery_charge):
    if skip_batteryc_tests:
        pytest.skip("No-BatteryC Option gesetzt")
    payload = {"battery_charge": battery_charge}
    response = session.post(getURL("/insert/battery-charge"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Akkustands Wert nicht in Range"}


@pytest.mark.usefixtures("skip_batteryc_tests")
@pytest.mark.parametrize("battery_charge", [6032.1, 490348204903.3, 100.1])
def test_batteryc_edge_cases_positive(skip_batteryc_tests, battery_charge):
    if skip_batteryc_tests:
        pytest.skip("No-BatteryC Option gesetzt")
    payload = {"battery_charge": battery_charge}
    response = session.post(getURL("/insert/battery-charge"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Akkustands Wert nicht in Range"}

@pytest.mark.usefixtures("skip_batteryc_tests")
def test_batteryc_edge_case_string(skip_batteryc_tests):
    if skip_batteryc_tests:
        pytest.skip("No-BatteryC Option gesetzt")
    payload = {"battery_charge": "hello"}
    response = session.post(getURL("/insert/battery-charge"), json=payload)
    assert response.status_code == 500


@pytest.mark.usefixtures("skip_batteryc_tests")
def test_batteryc_edge_case_wrong_key(skip_batteryc_tests):
    if skip_batteryc_tests:
        pytest.skip("No-BatteryC Option gesetzt")
    payload = {"dooomas": 50.2}
    response = session.post(getURL("/insert/battery-charge"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_batteryc_tests")
def test_batteryc_edge_case_wrong_timestamp(skip_batteryc_tests):
    if skip_batteryc_tests:
        pytest.skip("No-BatteryC Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "battery_charge": 18.1}
    response = session.post(getURL("/insert/battery-charge"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}


#############################################################################################################
# Batterie Spannungs Tests

@pytest.mark.usefixtures("skip_batteryv_tests")
@pytest.mark.parametrize("battery_voltage", [-60.1, -490348204903.3, -0.1])
def test_batteryv_edge_cases_negative(skip_batteryv_tests, battery_voltage):
    if skip_batteryv_tests:
        pytest.skip("No-BatteryV Option gesetzt")
    payload = {"battery_voltage": battery_voltage}
    response = session.post(getURL("/insert/battery-voltage"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Batteriespannungs Wert nicht in Range"}

@pytest.mark.usefixtures("skip_batteryv_tests")
@pytest.mark.parametrize("battery_voltage",  [6032.1, 490348204903.3, 4.6])
def test_batteryv_edge_cases_positve(skip_batteryv_tests, battery_voltage):
    if skip_batteryv_tests:
        pytest.skip("No-BatteryV Option gesetzt")
    payload = {"battery_voltage": battery_voltage}
    response = session.post(getURL("/insert/battery-voltage"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input! Batteriespannungs Wert nicht in Range"}


@pytest.mark.usefixtures("skip_batteryv_tests")
def test_batteryv_edge_cases_string(skip_batteryv_tests):
    if skip_batteryv_tests:
        pytest.skip("No-BatteryV Option gesetzt")
    payload = {"battery_voltage": "battery_voltage"}
    response = session.post(getURL("/insert/battery-voltage"), json=payload)
    assert response.status_code == 500



@pytest.mark.usefixtures("skip_batteryv_tests")
def test_batteryv_edge_cases_wrong_key(skip_batteryv_tests):
    if skip_batteryv_tests:
        pytest.skip("No-BatteryV Option gesetzt")
    payload = {"hello": 2.1}
    response = session.post(getURL("/insert/battery-voltage"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falscher Input!"}

@pytest.mark.usefixtures("skip_batteryv_tests")
def test_batteryv_edge_cases_wrong_timestamp(skip_batteryv_tests):
    if skip_batteryv_tests:
        pytest.skip("No-BatteryV Option gesetzt")
    payload = {"timestamp": "19:32:23 2024-02-23", "battery_voltage": 2.1}
    response = session.post(getURL("/insert/battery-voltage"), json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Falsches Timestamp-Format! Richtiges Format: '%Y-%m-%d %H:%M:%S'"}

if __name__ == '__main__':
    pytest.main()
