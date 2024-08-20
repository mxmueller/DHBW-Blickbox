import pytest
import os
from dotenv import load_dotenv
import docker
import time
from docker.errors import BuildError, ContainerError, APIError
load_dotenv()
def pytest_addoption(parser):
    parser.addoption("--noTemp", action="store_true", default=False, help="Überspringe Temperatur-Tests")
    parser.addoption("--noPing", action="store_true", default=False, help="Überspringe Ping-Tests")
    parser.addoption("--noHumid", action="store_true", default=False, help="Überspringe Luftfeuftigkeits-Tests")
    parser.addoption("--noWindDir", action="store_true", default=False, help="Überspringe Windrichtungs-Tests")
    parser.addoption("--noWindSpeed", action="store_true", default=False, help="Überspringe Windgeschwindigkeits-Tests")
    parser.addoption("--noRain", action="store_true", default=False, help="Überspringe Niederschlag-Tests")
    parser.addoption("--noBatteryC", action="store_true", default=False, help="Überspringe Batterieladungs-Tests")
    parser.addoption("--noBatteryV", action="store_true", default=False, help="Überspringe Batteriespannungs-Tests")



@pytest.fixture
def skip_ping_tests(request):
    return request.config.getoption("--noPing")

@pytest.fixture
def skip_temp_tests(request):
    return request.config.getoption("--noTemp")

@pytest.fixture
def skip_humid_tests(request):
    return request.config.getoption("--noHumid")

@pytest.fixture
def skip_winddir_tests(request):
    return request.config.getoption("--noWindDir")

@pytest.fixture
def skip_windspeed_tests(request):
    return request.config.getoption("--noWindSpeed")


@pytest.fixture
def skip_rain_tests(request):
    return request.config.getoption("--noRain")

@pytest.fixture
def skip_batteryc_tests(request):
    return request.config.getoption("--noBatteryC")

@pytest.fixture
def skip_batteryv_tests(request):
    return request.config.getoption("--noBatteryV")


@pytest.fixture(scope="session", autouse=True)
def docker_container():
    use_dev_container = os.getenv("API_USE_DEV_CONTAINER", "false").lower() == "true"
    if not use_dev_container:
        #pytest.skip("Production Routen werden genutzt. Container bauen ist irrelevant.")
        yield None
        return
    client = docker.from_env()
    try:
        image, logs = client.images.build(path="../", dockerfile="Dockerfile", tag="api-test:latest")
        for log in logs:
            print(log.get('stream', '').strip())
    except BuildError as e:
        pytest.fail(f"Build failed: {e.msg}")
        


    try:
        container = client.containers.run(
            image.id,
            detach=True,
            name="api-test",
            ports={'5000/tcp': 5000}
        )
    except ContainerError as e:
        pytest.fail(f"Container failed to start: {e}")    
    except APIError as e:
        pytest.fail(f"API error when starting the container: {e}")

    time.sleep(5)  
    yield container  

    container.stop()
    container.remove()


    client.images.remove(image.id)
