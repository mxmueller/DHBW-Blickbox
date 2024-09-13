from datetime import datetime, timedelta




onlinestatus = {
                "Valentin-Online" : {"online" : True, "timestamp" : "1970-1-1 00:00:00"}, 
                "Grafana-Online" : {"online" : True, "timestamp" : "1970-1-1 00:00:00"}, 
                "Database-Online" : {"online" : True, "timestamp" : "1970-1-1 00:00:00"}, 
                "ADA-Online": {"online" : True, "timestamp" : "1970-1-1 00:00:00"},
                "SARA-Online": {"online" : True, "timestamp" : "1970-1-1 00:00:00"}
                }


def update_online_status():
    global onlinestatus
    now = datetime.now()
    
    time_difference = timedelta(minutes=20)
    
    for key, value in onlinestatus.items():
        timestamp = datetime.strptime(value["timestamp"], "%Y-%m-%d %H:%M:%S")
        
        if now - timestamp > time_difference:
            onlinestatus[key]["online"] = False


def test_update_online_status():
    assert onlinestatus["Valentin-Online"]['online'] == True
    assert onlinestatus["ADA-Online"]['online'] == True
    assert onlinestatus["Database-Online"]['online'] == True
    assert onlinestatus["Grafana-Online"]['online'] == True
    assert onlinestatus["SARA-Online"]['online'] == True
    update_online_status()
    assert onlinestatus["Valentin-Online"]['online'] == False
    assert onlinestatus["ADA-Online"]['online'] == False
    assert onlinestatus["Database-Online"]['online'] == False
    assert onlinestatus["Grafana-Online"]['online'] == False
    assert onlinestatus["SARA-Online"]['online'] == False

