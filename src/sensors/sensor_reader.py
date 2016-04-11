try:
    import queue
except ImportError:
    import Queue as queue
import syslog


class SensorReader:
    def __init__(self, sensor_type, sensor):
        self.sensor_type = sensor_type
        self.sensor = sensor
        self.sensor_queue = queue.Queue(maxsize=0)
        self.latest_value = 0.0

    def read(self):
        """
        queries the sensor / attempts a read
        returns a dictionary where the key is the data type read and the value is the read value. defaults to value of
        0.0 if timeout exceeded before the device writes or responds.
        """
        self.latest_value = self.sensor.get_data()
        self.sensor_queue.put_nowait(self.latest_value)
        if self.sensor_queue.qsize() > 10:
            syslog.syslog(syslog.LOG_ALERT, "warning: %s queue size %d", self.sensor_type, self.sensor_queue.qsize())
            if __debug__:
                print("warning: %s queue size %d", self.sensor_type, self.sensor_queue.qsize())

        return self.latest_value

    def peek_latest(self):
        """
        returns the latest data node dictionary where the key is the data type read and the value is the last read
        value
        """
        return self.latest_value

    def pop_latest(self, timeout=1.0):
        """
        pulls the latest data node off the queue, up to the specified timeout. useful for logging / processing
        of data nodes.
        returns the data node, or `None` if timeout exceeded.
        """
        return self.sensor_queue.get(timeout=timeout)

    def get_keys(self):
        """
        returns the keys for the sensor provided
        """
        return self.sensor.get_keys()
