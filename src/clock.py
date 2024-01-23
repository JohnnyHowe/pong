import time

class _Clock:

    dt_seconds = None
    time_running_seconds = None

    def __init__(self):
        self.time_running_seconds = 0
        self._last_frame_time = time.time()
        self.dt_seconds = 1.0 / 60; # a safe default

    def tick(self):
        time_now = time.time()
        self.dt_seconds = time_now - self._last_frame_time
        self.time_running_seconds += self.dt_seconds
        self._last_frame_time = time_now

clock = _Clock()