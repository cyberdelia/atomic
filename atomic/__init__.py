from __future__ import with_statement

import multiprocessing
import threading

__all__ = ["Atomic"]


class Lock(object):
    def __init__(self, multiprocess=False):
        self.multiprocess = multiprocess
        if multiprocess:
            self.lock = multiprocessing.RLock()
        else:
            self.lock = threading.RLock()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()

    def acquire(self, block=True):
        if self.multiprocess:
            return self.lock.acquire(block=block)
        return self.lock.acquire(blocking=block)

    def release(self):
        return self.lock.release()


class Atomic(object):
    def __init__(self, value=None, multiprocess=False):
        self.lock = Lock(multiprocess=multiprocess)
        self._value = value

    def get_value(self):
        return self.get()

    def set_value(self, value):
        return self.set(value)

    value = property(get_value, set_value)

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

    def swap(self, new_value):
        return self.get_and_set(new_value)

    def compare_and_set(self, old_value, new_value):
        if not self.lock.acquire(block=False):
            return False
        try:
            if self._value != old_value:
                return False
            self._value = new_value
        finally:
            self.lock.release()
        return True

    def compare_and_swap(self, old_value, new_value):
        return self.compare_and_set(old_value, new_value)
