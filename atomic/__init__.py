from __future__ import with_statement

import multiprocessing
import threading

__all__ = ["Atomic", "ConcurrentUpdateError"]


class ConcurrentUpdateError(threading.ThreadError):
    pass


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


class AtomicUpdate(object):
    def __init__(self, atomic, value, retry=True):
        self._atomic = atomic
        self._old_value = value
        self.value = value
        self._retry = retry

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        old_value = self._old_value
        new_value = self.value
        if not self._retry:
            if not self._atomic.compare_and_set(old_value, new_value):
                raise ConcurrentUpdateError("Update failed")
        else:
            while self._atomic.compare_and_set(old_value, new_value):
                pass


class Atomic(object):
    def __init__(self, value=None, multiprocess=False):
        self.lock = Lock(multiprocess=multiprocess)
        self._value = value

    def get_value(self):
        return self.get()

    def set_value(self, value):
        return self.set(value)

    value = property(get_value, set_value)

    def update(self, retry=True):
        return AtomicUpdate(self, self.get(), retry)

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
