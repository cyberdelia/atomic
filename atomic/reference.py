import threading


class Reference(object):
    def __init__(self, value=None):
        self.lock = threading.RLock()
        self._value = value

    def __enter__(self):
        with self.lock:
            yield self

    def __exit__(self, type, value, traceback):
        pass

    def get(self):
        with self.lock:
            return self._value

    def set(self, value):
        with self.lock:
            self._value = value

    def get_and_set(self, new_value):
        with self.lock:
            old_value = self._value
            self._value = new_value
            return old_value

    def compare_and_set(self, expect_value, new_value):
        if not self.lock.acquire():
            return False
        try:
            if self._value != expect_value:
                return False
            self._value = new_value
        finally:
            self.lock.release()
        return True
