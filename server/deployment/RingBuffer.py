from collections import deque
from datetime import datetime
import json

class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = deque(maxlen=size)

    def append(self, item):
        self.buffer.append(item)

    def is_empty(self):
        return len(self.buffer) == 0

    def is_full(self):
        return len(self.buffer) == self.size

    def get_contents(self):
        return list(self.buffer)

def log(title, message, type, ringbuffer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {'title': title, 'message': message, 'type': type, 'timestamp': timestamp}
    ringbuffer.append(json.dumps(log_entry))

def check_and_send_new_entries(ring_buffer, socket):
    new_entries = []

    if not ring_buffer.is_empty():
        while not ring_buffer.is_empty():
            new_entry = ring_buffer.buffer.popleft()
            new_entries.append(json.loads(new_entry))

        for entry in new_entries:
            socket.send(entry)



def send_entires(ring_buffer, socket):
    for logs in ring_buffer.buffer:
        socket.send(json.loads(logs))
    