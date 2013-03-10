import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

from atomic import Atomic, ConcurrentUpdateException
from atomic.reference import Reference as py_reference

try:
    import atomic._reference
except ImportError as e:
    c_reference = None
else:
    c_reference = atomic._reference.Reference

is_jython = sys.platform.startswith("java")
if is_jython:
    from com.lapanthere.atomic import Reference as java_reference
else:
    java_reference = None  # noqa


class AtomicTest(object):
    def setUp(self):
        reference_cls = self._reference

        class MockAtomic(Atomic):
            def __init__(self, value=None):
                self.ref = reference_cls(value)
        self.atomic_cls = MockAtomic

    def test_init(self):
        atomic = self.atomic_cls()
        self.assertEqual(None, atomic.value)

        atomic = self.atomic_cls(0)
        self.assertEqual(0, atomic.value)

    def test_value(self):
        atomic = self.atomic_cls(0)
        atomic.value = 1
        self.assertEqual(1, atomic.value)

    def test_swap(self):
        atomic = self.atomic_cls(1000)
        swapped = atomic.swap(1001)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1000, swapped)

    def test_update(self):
        atomic = self.atomic_cls(1000)
        value = atomic.update(lambda v: v + 1)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1001, value)

    def test_try_update(self):
        atomic = self.atomic_cls(1000)
        value = atomic.try_update(lambda v: v + 1)
        self.assertEqual(1001, atomic.value)
        self.assertEqual(1001, value)
        reference = atomic.ref

        class MockReference(object):
            def get(self):
                return reference.get()

            def compare_and_set(self, old_value, new_value):
                return False

        atomic.ref = MockReference()
        with self.assertRaises(ConcurrentUpdateException):
            atomic.try_update(lambda v: v + 1)

    def test_complex_value(self):
        atomic = self.atomic_cls([-1, 0])
        self.assertEqual([-1, 0], atomic.value)

    def test_complex_update(self):
        def complex_update(v):
            return [v + 1 for v in v]
        atomic = self.atomic_cls([-1, 0])
        value = atomic.update(complex_update)
        self.assertEqual([0, 1], atomic.value)
        self.assertEqual([0, 1], value)


class PyAtomicTest(AtomicTest, unittest.TestCase):
    _reference = py_reference


@unittest.skipUnless(c_reference, "requires the C _reference module")
class CAtomicTest(AtomicTest, unittest.TestCase):
    _reference = c_reference

    def test_loaded(self):
        self.assertIsInstance(Atomic().ref, self._reference)


@unittest.skipUnless(is_jython, "requires Jython")
class JythonAtomicTest(AtomicTest, unittest.TestCase):
    _reference = java_reference

    def test_loaded(self):
        self.assertIsInstance(Atomic().ref, self._reference)
