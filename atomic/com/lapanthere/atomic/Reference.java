package com.lapanthere.atomic;

import java.util.concurrent.atomic.AtomicReferenceFieldUpdater;
import org.python.core.PyObject;


public class Reference {
    private volatile PyObject reference;
    private final static AtomicReferenceFieldUpdater<Reference, PyObject> ATOMIC =
        AtomicReferenceFieldUpdater.newUpdater(Reference.class, PyObject.class, "reference");

    public Reference(PyObject value) {
        this.reference = value;
    }
    
    public PyObject get() {
        return ATOMIC.get(this);
    }

    public PyObject set(PyObject value) {
        ATOMIC.set(this, value);
        return value;
    }

    public boolean compare_and_set(PyObject expectValue, PyObject newValue) {
        return ATOMIC.compareAndSet(this, expectValue, newValue);
    }

    public PyObject get_and_set(PyObject value) {
        return ATOMIC.getAndSet(this, value);
    }
}