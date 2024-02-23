import unittest
import requests
import time
import sys

def getURL(path):
    return ("http://dhbwapi.maytastix.de/iot/api" + path)


def parseOption():
    global noping
    global notemp
    global nohumid
    global nowindspeed
    global nowinddir  
    noping = False
    notemp = False
    nohumid = False
    nowindspeed = False
    nowinddir = False
    if(len(sys.argv) < 2):
        return
    validoptions = 0
    for x in sys.argv:
        if x == "noping":
            noping = True
            validoptions +=1
        elif x == "notemp":
            notemp = True
            validoptions +=1 
        elif x == "nohumid":
            nohumid = True
            validoptions +=1
        elif x == "nowindspeed":
            nowindspeed = True
            validoptions +=1
        elif x == "nowinddir":
            nowinddir = True
            validoptions +=1

        else:
            continue
    if(validoptions == 0):
        print("no valid option found! valid options are: noping, notemp, nohumid, nowindspeed, nowinddir")
        exit(0)




class TestDatabaseAPI(unittest.TestCase):
    
    # Test ob die Influx Datenbank verbunden ist.
    def test_db_status(self):
        if(noping):
            return
        response = requests.get(getURL("/pingDB"))
        self.assertEqual(response.status_code, 200)
        expected_data = {'message': 'Verbingung zur Datenbank steht'}
        actual_data = response.json()
        self.assertEqual(actual_data, expected_data)
    
    # Test ob der Grafana Server läuft
    def test_grafana_status(self):
        if(noping):
            return
        response = requests.get(getURL("/pingGF"))
        self.assertEqual(response.status_code, 200)
        expected_data = {'message': 'Verbingung zu Grafana steht'}
        actual_data = response.json()
        self.assertEqual(actual_data, expected_data)

    
    ##################################################################
    # Temperatur Unit-Tests

    # Range Tests Negative Zahlen
    def test_temperature_edge_casesN1(self):
        if(notemp):
            return
        payload = {"temperature": -60.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Temperatur nicht in Range"}
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_temperature_edge_casesN2(self):
        if(notemp):
            return
        payload = {"temperature": -490348204903.3}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Temperatur nicht in Range"}
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    # Range Tests Positve Zahlen
    def test_temperature_edge_casesP1(self):
        if(notemp):
            return
        payload = {"temperature": 100.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Temperatur nicht in Range"}
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)

    def test_temperatrue_edge_casesP2(self):
        if(notemp):
            return
        payload = {"temperature": 44343532.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Temperatur nicht in Range"}
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)

    # Test ob die API strings Blockiert
    def test_temperature_edge_casesString(self):
        if(notemp):
            return
        payload = {"temperature": "hello"}
        expected_status_code = 500
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)

    def test_temperature_WrongKey(self):
        if(notemp):
            return
        payload = {"air-humidity": 18.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input!"}
        response = requests.post(getURL("/insert/temperature"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    ##########################################################################
    # Luftfeuchtigkeits Unit-Tests
    def test_airhumidity_edge_casesN1(self):
        if(nohumid):
            return
        payload = {"air-humidity": -0.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_airhumidity_edge_casesN2(self):
        if(nohumid):
            return
        payload = {"air-humidity": -100}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)

    def test_airhumidity_edge_casesP1(self):
        if(nohumid):
            return
        payload = {"air-humidity": 100.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_airhumidity_edge_casesP2(self):
        if(nohumid):
            return
        payload = {"air-humidity": 44343532.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Luftfeuchtigkeit nicht in Range"}
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)

    def test_airhumidity_edge_casesString(self):
        if(nohumid):
            return
        payload = {"air-humidity": "hello"}
        expected_status_code = 500
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)

    def test_airhumidity_WrongKey(self):
        if(nohumid):
            return
        payload = {"temperature": 18.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input!"}
        response = requests.post(getURL("/insert/air-humidty"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)


    ################################################################################
    #Wind-Speed Unit Tests
    def test_wind_speed_edge_casesN1(self):
        if(nowindspeed):
            return
        payload = {"wind-speed": -0.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
        
    def test_wind_speed_edge_casesN2(self):
        if(nowindspeed):
            return
        payload = {"wind-speed": -1000}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_wind_speed_edge_casesP1(self):
        if(nowindspeed):
            return
        payload = {"wind-speed": 500.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_wind_speed_edge_casesP2(self):
        if(nowindspeed):
            return
        payload = {"wind-speed": 44343532.1}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input! Windgeschwindigkeit nicht in Range"}
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)
    
    def test_wind_speed_edge_casesP2(self):
        if(nowindspeed):
            return
        payload = {"wind-speed": "hello"}
        expected_status_code = 500
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)


    def test_wind_speed_edge_casesP1(self):
        if(nowindspeed):
            return
        payload = {"hallo": 50}
        expected_status_code = 400
        expected_data = {"message": "Falscher Input!"}
        response = requests.post(getURL("/insert/wind-speed"), json=payload)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json(), expected_data)

if __name__ == '__main__':
    parseOption()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
