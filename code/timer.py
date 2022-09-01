"""
Exports Timer class for simple timekeeping and timeout management
"""
import time

class Timer:
    """
    A class representing a stopwatch-like timer.
    """

    def __init__(self):
        self._elapsed = 0
        self._start = 0
        self._timeout = -1
        self._running = False

    def start(self):
        " Start timer if not running "
        if not self._running:
            self._start = time.time()
            self._running = True
        return self

    def restart(self):
        " Restart timer (stop then start) "
        self.reset()
        self.start()
        return self

    def reset(self):
        " Stop timer and reset timer values "
        self._elapsed = 0
        self._start = 0
        self._running = False
        return self

    def stop(self):
        " Alias for reset() "
        self.reset()
        return self

    def elapsed(self):
        " Get time elapsed from start "
        return time.time() - self._start

    def set_timeout(self, s = -1):
        " Set a timeout for the timer "
        self._timeout = s
        return self

    def timed_out(self):
        " Get status of timeout "
        return self._timeout > self._elapsed
