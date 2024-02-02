import time

from .easings import lerp

class _Clock:

    dt_seconds = None
    time_running_seconds = None
    instant_fps = 60
    smoothed_fps = 60
    min_fps = 30

    def __init__(self):
        self.time_running_seconds = 0
        self._last_frame_time = time.time()
        self.dt_seconds = 1.0 / self.min_fps 

    def tick(self):
        time_now = time.time()
        self.dt_seconds = time_now - self._last_frame_time
        if (self.dt_seconds == 0): self.dt_seconds = 1.0 / self.min_fps
        self.dt_seconds = min(self.dt_seconds, 1.0 / self.min_fps)

        self.time_running_seconds += self.dt_seconds
        self._last_frame_time = time_now

        self.instant_fps = 1 / self.dt_seconds
        self.smoothed_fps = lerp(self.smoothed_fps, self.instant_fps, 0.1)

clock = _Clock()