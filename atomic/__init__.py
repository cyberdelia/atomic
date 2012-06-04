import threading

__all__ = ["Atomic", "ConcurrentUpdateException"]


try:
    try:
        from com.lapanthere.atomic import Reference
    except ImportError:
        from atomic._reference import Reference  # noqa
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


class ConcurrentUpdateException(Exception):
    pass


class Atomic(object):
    """
    An atomic class that guarantees atomic updates to its contained value.
    """
    def __init__(self, value=None):
        """
        Creates a new Atomic with the given initial value.

        :param value: initial value
        """
        self.ref = Reference(value)

    def get_value(self):
        return self.ref.get()

    def set_value(self, value):
        return self.ref.set(value)

    value = property(get_value, set_value, doc="""Get or set current value""")

    def get_and_set(self, new_value):
        """Atomically sets to the given value and returns the old value

        :param new_value: the new value
        """
        return self.ref.get_and_set(new_value)

    def swap(self, new_value):
        return self.get_and_set(new_value)

    def compare_and_set(self, expect_value, new_value):
        """
        Atomically sets the value to the given value if the current value is
        equal to the expected value.

        :param expect_value: the expected value
        :param new_value: the new value
        """
        return self.ref.compare_and_set(expect_value, new_value)

    def compare_and_swap(self, expect_value, new_value):
        return self.compare_and_set(expect_value, new_value)

    def update(self, update_func):
        """
        Update value based on the given function.

        It may run the block repeatedly if there are other concurrent
        updates in progress.

        :param update_func: a function that given the current value
            return the new value
        :type update_func: func
        """
        update = False
        while not update:
            old_value = self.ref.get()
            new_value = update_func(old_value)
            update = self.ref.compare_and_set(old_value, new_value)
        return new_value

    def try_update(self, update_func):
        """
        Update value based on the given function.

        If the value changes before the update can happen,
        it will raise a :class:`ConcurrentUpdateException`.

        :param update_func: a function that given the current
            value return the new value
        :type update_func: func
        :raises: ConcurrentUpdateException
        """
        old_value = self.ref.get()
        new_value = update_func(old_value)
        while not self.ref.compare_and_set(old_value, new_value):
            raise ConcurrentUpdateException("Updating reference failed")
        return new_value
