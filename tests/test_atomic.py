try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

from atomic import AtomicLong, AtomicLongArray


class AtomicLongTest(unittest.TestCase):
    def test_init(self):
        atomic = AtomicLong()
        self.assertEqual(0, atomic.value)

        atomic = AtomicLong(0)
        self.assertEqual(0, atomic.value)

    def test_value(self):
        atomic = AtomicLong(0)
        atomic.value = 1
        self.assertEqual(1, atomic.value)

    def test_swap(self):
        atomic = AtomicLong(1000)
        swapped = atomic.swap(1001)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1000, swapped)

    def test_compare_and_swap(self):
        atomic = AtomicLong(1000)
        swapped = atomic.compare_and_swap(1000, 1001)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(True, swapped)

        swapped = atomic.compare_and_swap(1000, 1024)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(False, swapped)

    def test_add(self):
        atomic = AtomicLong(1000)
        atomic += 1
        self.assertEqual(1001, atomic.value)

    def test_sub(self):
        atomic = AtomicLong(1000)
        atomic -= 1
        self.assertEqual(999, atomic.value)

class AtomicLongArrayTest(unittest.TestCase):
    def test_init(self):
        atomic = AtomicLongArray()
        self.assertEqual([], atomic.value)

        atomic = AtomicLongArray([-1, 0])
        self.assertEqual([-1, 0], atomic.value)

    def test_value(self):
        atomic = AtomicLongArray([])
        atomic.value = [-1, 0]
        self.assertEqual([-1, 0], atomic.value)

    def test_get(self):
        atomic = AtomicLongArray([-1, 0])
        self.assertEqual(atomic[0], -1)
        self.assertEqual(atomic[1], 0)

    def test_set(self):
        atomic = AtomicLongArray([-1, 0])
        atomic[1] = -2
        self.assertEqual(atomic[1], -2)

    def test_set_obj(self):
        atomic = AtomicLongArray([-1, 0])
        atomic[1] = AtomicLong(-2)
        self.assertEqual(atomic[1], -2)

    def test_increment(self):
        atomic = AtomicLongArray([-1, 0])
        atomic[1] += 1
        self.assertEqual(atomic[1], 1)

    def test_iter(self):
        atomic = AtomicLongArray([-1, 0])
        for i, a in enumerate(atomic):
            self.assertEqual(atomic[i], a)
