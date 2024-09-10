import docker
import pytest
import time
import os
import requests
from dotenv import load_dotenv
load_dotenv()

use_dev_container = os.getenv("API_USE_DEV_CONTAINER", "false").lower() == "true"

def getURL(path):
    return "http://localhost:5000/iot/api" + path



session = requests.Session()
session.headers.update({"blickbox": "true"})



# Nach restart sollte alles wieder funktionieren--> Wenn Container stirbt dann wird der in Prod automatisch neu gestartet
def test_container_restart():
    if not use_dev_container:
        pytest.skip("Dieser Test klappt nur in Test-Umgebungen")
    client = docker.from_env()
    container = client.containers.get('api-test')
    container.restart()
    payload = {"temperature": "hello"}
    with pytest.raises(Exception):
        response = session.post(getURL("/insert/temperature"), json=payload)

    time.sleep(5)  
    container.reload()
    assert container.status == "running"  
    payload = {"temperature": "hello"}
    response = session.post(getURL("/insert/temperature"), json=payload)
    assert response.status_code == 500
