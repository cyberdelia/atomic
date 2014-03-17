======
Atomic
======

An atomic class that guarantees atomic updates to its contained value. ::

    from atomic import AtomicLong
    atomic = AtomicLong(0)
    atomic += 1
    atomic.value


Installation
============

To install atomic, use pip : ::

    pip install atomic


Acknowledgement
===============

This is heavily inspired by `ruby-atomic <https://github.com/headius/ruby-atomic>`_.
