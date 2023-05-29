import threading
import time
import random
import signal
import sqlite3
import datetime


class Sensor:
    def __init__(self, sensor_id: int, sensor_high: float, sensor_low: float, sensor_wait: int):
        self.id = sensor_id
        self.high = sensor_high
        self.low = sensor_low
        self.time_to_wait = sensor_wait
        

    def run(self):
        con = sqlite3.connect('measurements.db')
        value = random.uniform(self.low, self.high)
        print(f"Sensor {self.id} generated value {value}")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"INSERT INTO Measurement(m_value, m_timestamp, s_id) VALUES({value}, '{timestamp}', {self.id})"
        con.cursor().execute(query)
        con.commit()
        con.close()
        time.sleep(self.time_to_wait)


exit_event = threading.Event()

def signal_handler(signum, frame):
    exit_event.set()

def sensor_runner(sensor_obj):
    while True:
        sensor_obj.run()
        if exit_event.is_set():
            break
    print("Bye!")



if __name__ == '__main__':
    sensors_lst = [
        Sensor(1, 5.5, 0, 30),
        Sensor(2, 30, -10, 60),
        Sensor(3, 30, 0, 60),
        Sensor(4, 0.1, 0, 30),
        Sensor(5, 1, 0, 30)
    ]
    threads_lst = list()

    signal.signal(signal.SIGINT, signal_handler)    

    for sensor in sensors_lst:
        thread = threading.Thread(target=sensor_runner, args=[sensor])
        thread.start()
        threads_lst.append(thread)

    for thread in threads_lst:
        thread.join()

    

