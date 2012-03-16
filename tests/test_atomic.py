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
        with atomic:
            atomic.value += 1
        self.assertEqual(1001, atomic.value)
