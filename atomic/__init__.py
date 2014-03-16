from cffi import FFI

ffi = FFI()

ffi.cdef("""
void long_store(long *, long *);
long long_add_and_fetch(long *, long);
long long_sub_and_fetch(long *, long);
long long_get_and_set(long *, long);
long long_compare_and_set(long *, long *, long);
""")

atomic = ffi.verify("""
void long_store(long *v, long *n) {
    __atomic_store(v, n, __ATOMIC_SEQ_CST);
};
long long_add_and_fetch(long *v, long i) {
    return __atomic_add_fetch(v, i, __ATOMIC_SEQ_CST);
};
long long_sub_and_fetch(long *v, long i) {
    return __atomic_sub_fetch(v, i, __ATOMIC_SEQ_CST);
};
long long_get_and_set(long *v, long n) {
    return __atomic_exchange_n(v, n, __ATOMIC_SEQ_CST);
};
long long_compare_and_set(long *v, long *e, long n) {
    return __atomic_compare_exchange_n(v, e, n, 0, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
};
""")


class AtomicLong(object):
    """
    An atomic class that guarantees atomic updates to its contained integer value.
    """
    def __init__(self, value=None):
        """
        Creates a new AtomicLong with the given initial value.

        :param value: initial value
        """
        self._value = ffi.new('long *', value)

    def __repr__(self):
        return '<{0} at 0x{1:x}: {2!r}>'.format(
            self.__class__.__name__, id(self), self.value)

    @property
    def value(self):
        return self._value[0]

    @value.setter
    def value(self, new):
        atomic.long_store(self._value, ffi.new('long *', new))

    def __iadd__(self, inc):
        atomic.long_add_and_fetch(self._value, inc)
        return self

    def __isub__(self, dec):
        atomic.long_sub_and_fetch(self._value, dec)
        return self

    def get_and_set(self, new_value):
        """Atomically sets to the given value and returns the old value

        :param new_value: the new value
        """
        return atomic.long_get_and_set(self._value, new_value)

    def swap(self, new_value):
        return self.get_and_set(new_value)

    def compare_and_set(self, expect_value, new_value):
        """
        Atomically sets the value to the given value if the current value is
        equal to the expected value.

        :param expect_value: the expected value
        :param new_value: the new value
        """
        return bool(atomic.long_compare_and_set(self._value, ffi.new('long *', expect_value), new_value))

    def compare_and_swap(self, expect_value, new_value):
        return self.compare_and_set(expect_value, new_value)


class AtomicLongArray(object):
    """
    An atomic class that guarantees atomic updates to its contained integer values.
    """
    def __init__(self, array=[]):
        """
        Creates a new AtomicLongArray with the given initial array of integers.

        :param array: initial values
        """
        self._array = [AtomicLong(x) for x in array]

    def __len__(self):
        return len(self._array)

    def __getitem__(self, key):
        return self._array[key].value

    def __setitem__(self, key, value):
        if self._array[key]:
            self._array[key].value = value
        else:
            self._array[key] = AtomicLong(value)

    def __iter__(self):
        for a in self._array:
            yield a.value

    @property
    def value(self):
        return [a.value for a in self._array]

    @value.setter
    def value(self, new=[]):
        self._array = [AtomicLong(int(x)) for x in new]
