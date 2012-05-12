from unittest import TestCase

from atomic import Atomic


class AtomicTest(TestCase):
    def test_init(self):
        atomic = Atomic()
        self.assertEqual(None, atomic.value)

        atomic = Atomic(0)
        self.assertEqual(0, atomic.value)

    def test_value(self):
        atomic = Atomic(0)
        atomic.value = 1
        self.assertEqual(1, atomic.value)

    def test_swap(self):
        atomic = Atomic(1000)
        swapped = atomic.swap(1001)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1000, swapped)

    def test_update(self):
        atomic = Atomic(1000)
        value = atomic.update(lambda v: v + 1)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1001, value)

    def test_try_update(self):
        atomic = Atomic(1000)
        value = atomic.try_update(lambda v: v + 1)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1001, value)

    def test_complex_value(self):
        atomic = Atomic([-1, 0])
        self.assertEqual([-1, 0], atomic.value)

    def test_complex_update(self):
        def complex_update(v):
            return [v + 1 for v in v]
        atomic = Atomic([-1, 0])
        value = atomic.update(complex_update)
        self.assertEqual([0, 1], atomic.value)
        self.assertEqual([0, 1], value)
