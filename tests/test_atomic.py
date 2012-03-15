from unittest import TestCase

from atomic import Atomic, ConcurrentUpdateError


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
        with atomic.update() as updater:
            updater.value += 1
        self.assertEqual(1001, atomic.value)

    def test_update_no_retry(self):
        atomic = Atomic(1000)
        with atomic.update(retry=False) as updater:
           updater.value += 1
        self.assertEqual(1001, atomic.value)

    def test_update_fail(self):
        atomic = Atomic(1000)
        def callable():
            with atomic.update(retry=False) as updater:
                atomic.value = 1001
                updater.value += 1
        self.assertRaises(ConcurrentUpdateError, callable)
            