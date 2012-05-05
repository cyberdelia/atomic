#include <Python.h>
#include "structmember.h"

typedef struct {
	PyObject_HEAD
	PyObject * value;
} Reference;

static void Reference_dealloc(Reference * self) {
	Py_XDECREF(self->value);
	Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject * Reference_new(PyTypeObject * type, PyObject * args, PyObject * kwds) {
	Reference *self;
	self = (Reference *) type->tp_alloc(type, 0);
	return (PyObject *) self;
}

static int Reference_init(Reference * self, PyObject * args, PyObject * kwds) {
	PyObject *value = NULL, *previous;
	if (!PyArg_ParseTuple(args, "O", &value)) {
		return -1;
	}
	previous = self->value;
	Py_INCREF(value);
	self->value = value;
	Py_XDECREF(previous);
	return 0;
}

static PyObject * Reference_get(Reference * self) {
	Py_INCREF(self->value);
	return self->value;
}

static PyObject * Reference_set(Reference * self, PyObject * args) {
	PyObject *new_value = NULL, *old_value;
	if (!PyArg_ParseTuple(args, "O", &new_value)) {
		return NULL;
	}
	old_value = self->value;
	Py_INCREF(new_value);
	self->value = new_value;
	Py_XDECREF(old_value);
	return Py_None;
}

static PyObject * Reference_get_and_set(Reference * self, PyObject * args) {
	PyObject *new_value = NULL, *old_value;
	if (!PyArg_ParseTuple(args, "O", &new_value)) {
		return NULL;
	}
	old_value = self->value;
	Py_INCREF(new_value);
	self->value = new_value;
	Py_XDECREF(old_value);
	return old_value;
}

static PyObject * Reference_compare_and_set(Reference * self, PyObject * args) {
	PyObject *expect_value = NULL, *new_value = NULL;
	if (!PyArg_ParseTuple(args, "OO", &expect_value, &new_value)) {
		return NULL;
	}
#if __ENVIRONMENT_MAC_OS_X_VERSION_MIN_REQUIRED__ >= 1050
	if (OSAtomicCompareAndSwap64(expect_value, new_value, &self->value)) {
		return Py_True;
	}
#elif defined(_MSC_VER)
	if (InterlockedCompareExchange(&self->value, new_value, old_value)) {
		return Py_True;
	}
#elif (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__) > 40100
	if (__sync_bool_compare_and_swap(&self->value, expect_value, new_value)) {
		return Py_True;
	}
#else
 #error No CAS operation available for this platform
#endif
	return Py_False;
}

static PyMethodDef Reference_methods[] = {
	{"get", (PyCFunction) Reference_get, METH_NOARGS, "Get value"},
	{"set", (PyCFunction) Reference_set, METH_VARARGS, "Set value"},
	{"get_and_set", (PyCFunction) Reference_get_and_set, METH_VARARGS, "Get and set value"},
	{"compare_and_set", (PyCFunction) Reference_compare_and_set, METH_VARARGS, "Compare and set value"},
	{NULL}
};

static PyTypeObject reference_ReferenceType = {
	PyObject_HEAD_INIT(NULL)
	0,
	"reference.Reference",
	sizeof(Reference),
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	"Reference",
	0,
	0,
	0,
	0,
	0,
	0,
	Reference_methods,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	(initproc) Reference_init,
	0,
	Reference_new,
};

static PyMethodDef reference_methods[] = {
	{NULL}
};

PyMODINIT_FUNC initreference(void) {
	PyObject *m;

	reference_ReferenceType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&reference_ReferenceType) < 0)
		return;

	m = Py_InitModule3("reference", reference_methods, "reference module");

	Py_INCREF(&reference_ReferenceType);
	PyModule_AddObject(m, "Reference", (PyObject *) & reference_ReferenceType);
}
