import threading

__all__ = ["Atomic", "ConcurrentUpdateException"]


try:
    from reference import Reference
except ImportError:
    class Reference(object):  # noqa
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

        def compare_and_set(self, old_value, new_value):
            if not self.lock.acquire():
                return False
            try:
                if self._value != old_value:
                    return False
                self._value = new_value
            finally:
                self.lock.release()
            return True


class ConcurrentUpdateException(Exception):
    pass


class Atomic(object):
    def __init__(self, value=None):
        self.ref = Reference(value)

    def get_value(self):
        return self.ref.get()

    def set_value(self, value):
        return self.ref.set(value)

    value = property(get_value, set_value)

    def get_and_set(self, new_value):
        return self.ref.get_and_set(new_value)

    def swap(self, new_value):
        return self.get_and_set(new_value)

    def compare_and_set(self, old_value, new_value):
        return self.ref.compare_and_set(old_value, new_value)

    def compare_and_swap(self, old_value, new_value):
        return self.compare_and_set(old_value, new_value)

    def update(self, update_func):
        update = False
        while not update:
            old_value = self.ref.get()
            new_value = update_func(old_value)
            update = self.ref.compare_and_set(old_value, new_value)
        return new_value

    def try_update(self, update_func):
        old_value = self.ref.get()
        new_value = update_func(old_value)
        while not self.ref.compare_and_set(old_value, new_value):
            raise ConcurrentUpdateException("Updating reference failed")
        return new_value
