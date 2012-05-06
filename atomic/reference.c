#include <Python.h>
#include "structmember.h"

typedef struct {
	PyObject_HEAD
	PyObject * value;
} Reference;

static int Reference_traverse(Reference * self, visitproc visit, void *arg) {
	int vret;
	if (self->value) {
		vret = visit(self->value, arg);
		if (vret != 0) {
			return vret;
		}
	}
	return 0;
}

static int Reference_clear(Reference * self) {
	Py_CLEAR(self->value);
	return 0;
}

static void Reference_dealloc(Reference * self) {
	Py_XDECREF(self->value);
	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject * Reference_new(PyTypeObject * type, PyObject * args, PyObject * kwds) {
	Reference *self;
	self = (Reference *) type->tp_alloc(type, 0);
	return (PyObject *) self;
}

static int Reference_init(Reference * self, PyObject * args, PyObject * kwds) {
	PyObject *value, *previous;
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

static PyObject * Reference_set(Reference * self, PyObject * args)
{
	PyObject *new_value, *old_value;
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
	PyObject *new_value, *old_value;
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
	PyObject *expect_value, *new_value;
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

static PyMethodDef reference_methods[] = {
	{"get", (PyCFunction) Reference_get, METH_NOARGS, "Get value"},
	{"set", (PyCFunction) Reference_set, METH_VARARGS, "Set value"},
	{"get_and_set", (PyCFunction) Reference_get_and_set, METH_VARARGS, "Get and set value"},
	{"compare_and_set", (PyCFunction) Reference_compare_and_set, METH_VARARGS, "Compare and set value"},
	{NULL}
};

static PyTypeObject ReferenceType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	0,
	"reference.Reference",
	sizeof(Reference),
	0,
	(destructor) Reference_dealloc,
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
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
	"Reference",
	(traverseproc) Reference_traverse,
	(inquiry) Reference_clear,
	0,
	0,
	0,
	0,
	reference_methods,
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

#if PY_MAJOR_VERSION >= 3
	static struct PyModuleDef reference_module = {
		PyModuleDef_HEAD_INIT,
		"reference",
		"Reference module.",
		-1,
		NULL, NULL, NULL, NULL, NULL
	};
	#define INITERROR return NULL
 	PyObject * PyInit_reference(void) {
#else
 	#define INITERROR return
	void initreference(void) {
#endif
#if PY_MAJOR_VERSION >= 3
	PyObject *module = PyModule_Create(&reference_module);
#else
	PyObject *module = Py_InitModule("reference", reference_methods);
#endif
	if (module == NULL) {
		INITERROR;
	}
#if PY_MAJOR_VERSION >= 3
	return module;
#endif
}
