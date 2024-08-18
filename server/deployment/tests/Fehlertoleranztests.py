import docker
import pytest
import time

client = docker.from_env()

CONTAINER_NAME = "api-test"


image, logs = client.images.build(path="../", dockerfile="Dockerfile", tag="api-test:latest")


for log in logs:
    print(log.get('stream', '').strip())


container = client.containers.run(
    image.id,
    detach=True,
    name="api-test",
    ports={'5000/tcp': 5000}
)


for line in container.logs(stream=True):
    print(line.decode('utf-8').strip())


for i in range(20):
    print(i)
    time.sleep(1)
print("before")
container.stop()
container.remove()
print("after")
# @pytest.fixture(scope="module")
# def container():

#     container = client.containers.get(CONTAINER_NAME)
#     yield container

#     # container.restart()


# def test_network_disconnect(container):
#     """Test how the container handles network disconnection."""
#     network = client.networks.get("bridge")
#     network.disconnect(container)

#     # Führe hier den Test durch, ob die Anwendung korrekt reagiert
#     time.sleep(5)  # Warte, um die Auswirkungen zu beobachten
#     assert container.status == "running"  # Beispiel-Check

#     network.connect(container)


# def test_cpu_stress(container):
#     """Test how the container handles CPU stress."""
#     container.exec_run("apt-get update && apt-get install -y stress")
#     container.exec_run("stress --cpu 2 --timeout 60")

#     # Führe hier den Test durch, ob die Anwendung korrekt funktioniert
#     assert container.status == "running"  # Beispiel-Check


# def test_memory_limit(container):
#     """Test how the container handles memory limit."""
#     container.update(mem_limit="256m")
#     container.exec_run("stress --vm 1 --vm-bytes 300M --timeout 60")

#     # Führe hier den Test durch, ob die Anwendung korrekt funktioniert
#     assert container.status == "running"  # Beispiel-Check


# def test_io_limit():
#     """Test how the container handles I/O limits."""
#     container = client.containers.run(
#         "dein-image",
#         name="io-test-container",
#         detach=True,
#         device_write_bps={"/dev/sda": "1mb"}
#     )

#     # Führe hier den Test durch, ob die Anwendung korrekt funktioniert
#     time.sleep(5)  # Warte, um die Auswirkungen zu beobachten
#     assert container.status == "running"  # Beispiel-Check

#     container.stop()
#     container.remove()


# def test_container_restart(container):
#     """Test how the container handles a restart."""
#     container.restart()

#     # Führe hier den Test durch, ob die Anwendung korrekt neu startet
#     time.sleep(5)  # Warte, um den Neustart abzuschließen
#     assert container.status == "running"  # Beispiel-Check


# # def test_dependent_service_failure():
# #     """Test how the container handles failure of a dependent service."""
# #     dependent_service = client.containers.get(DEPENDENT_SERVICE_NAME)
# #     dependent_service.stop()

# #     # Führe hier den Test durch, ob die Anwendung korrekt reagiert
# #     container = client.containers.get(CONTAINER_NAME)
# #     time.sleep(5)  # Warte, um die Auswirkungen zu beobachten
# #     assert container.status == "running"  # Beispiel-Check

# #     dependent_service.start()
