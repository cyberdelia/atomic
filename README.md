# Atomic

An atomic class that guarantees atomic updates to its contained value.

    >>> from atomic import Atomic
    >>> atomic = Atomic(0)
    >>> atomic.value = 40
    >>> atomic.value
    40
    >>> with atomic:
        atomic.value += 1
    >>> atomic.value
    41
   


## Installation

To install atomic, use pip :

    $ pip install atomic

## Acknowledgement

This is heavily inspired by [ruby-atomic](https://github.com/headius/ruby-atomic).
