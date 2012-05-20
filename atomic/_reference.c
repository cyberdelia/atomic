#include <Python.h>
#include "structmember.h"

typedef struct Reference {
	PyObject_HEAD
	PyObject * value;
} Reference;

static int Reference_traverse(Reference * self, visitproc visit, void *arg) {
	Reference *s;
	s = (Reference *)self;
	Py_VISIT(s->value);
	return 0;
}

static int Reference_clear(Reference * self) {
	Reference *s;
	s = (Reference *)self;
	Py_CLEAR(s->value);
	return 0;
}

static void Reference_dealloc(Reference * self) {
	Reference_clear(self);
	Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject * Reference_new(PyTypeObject * type, PyObject * args, PyObject * kwds) {
	Reference *self;
	self = (Reference *) type->tp_alloc(type, 0);
	if (self != NULL) {
			self->value = NULL;
	}
	return (PyObject *) self;
}

static int Reference_init(Reference * self, PyObject * args, PyObject * kwds) {
	PyObject *value;
	if (!PyArg_ParseTuple(args, "O", &value)) {
		return -1;
	}
	self->value = value;
	Py_INCREF(self->value);
	return 0;
}

static PyObject * Reference_get(Reference * self) {
	Py_INCREF(self->value);
	return self->value;
}

static PyObject * Reference_set(Reference * self, PyObject * args)
{
	PyObject *new_value;
	if (!PyArg_ParseTuple(args, "O", &new_value)) {
		return NULL;
	}
	self->value = new_value;
	Py_INCREF(self->value);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject * Reference_get_and_set(Reference * self, PyObject * args) {
	PyObject *new_value, *old_value;
	if (!PyArg_ParseTuple(args, "O", &new_value)) {
		return NULL;
	}
	old_value = self->value;
	self->value = new_value;
	Py_INCREF(self->value);
	Py_INCREF(old_value);
	return old_value;
}

static PyObject * Reference_compare_and_set(Reference * self, PyObject * args) {
	PyObject *expect_value, *new_value;
	if (!PyArg_ParseTuple(args, "OO", &expect_value, &new_value)) {
		return NULL;
	}
	Py_INCREF(self->value);
	Py_INCREF(expect_value);
	Py_INCREF(new_value);
#if __ENVIRONMENT_MAC_OS_X_VERSION_MIN_REQUIRED__ >= 1050
	if (OSAtomicCompareAndSwap64(expect_value, new_value, &self->value)) {
		Py_INCREF(Py_True);
		return Py_True;
	}
#elif defined(_MSC_VER)
	if (InterlockedCompareExchange(&self->value, new_value, old_value)) {
		Py_INCREF(Py_True);
		return Py_True;
	}
#elif (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__) > 40100
	if (__sync_bool_compare_and_swap(&self->value, expect_value, new_value)) {
		Py_INCREF(Py_True);
		return Py_True;
	}
#else
#error No CAS operation available for this platform
#endif
	Py_INCREF(Py_False);
	return Py_False;
}

static PyMemberDef reference_members[] = {
		{"value", T_OBJECT, offsetof(Reference, value), READONLY, "value"},
		{NULL}
};


static PyMethodDef reference_methods[] = {
	{"get", (PyCFunction) Reference_get, METH_NOARGS, "Get value"},
	{"set", (PyCFunction) Reference_set, METH_VARARGS, "Set value"},
	{"get_and_set", (PyCFunction) Reference_get_and_set, METH_VARARGS, "Get and set value"},
	{"compare_and_set", (PyCFunction) Reference_compare_and_set, METH_VARARGS, "Compare and set value"},
	{NULL}
};

#ifndef PyVarObject_HEAD_INIT
		#define PyVarObject_HEAD_INIT(type, size) \
				PyObject_HEAD_INIT(type) size,
#endif

static PyTypeObject ReferenceType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"atomic._reference.Reference",
	sizeof(Reference),
	0,
	Reference_dealloc,
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
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
	"Atomic reference object",
	Reference_traverse,
	Reference_clear,
	0,
	0,
	0,
	0,
	reference_methods,
	reference_members,
	0,
	0,
	0,
	0,
	0,
	0,
	(initproc) Reference_init,
	0,
	Reference_new,
	0,
};

#if PY_MAJOR_VERSION >= 3
	#define MOD_ERROR_VAL NULL
	#define MOD_SUCCESS_VAL(val) val
	#define MOD_INIT(name) PyMODINIT_FUNC PyInit__##name(void)
	#define MOD_DEF(ob, name, doc) \
		static struct PyModuleDef moduledef = { \
			PyModuleDef_HEAD_INIT, name, doc, -1}; \
		ob = PyModule_Create(&moduledef);
#else
	#define MOD_ERROR_VAL
	#define MOD_SUCCESS_VAL(val)
	#define MOD_INIT(name) void init_##name(void)
	#define MOD_DEF(ob, name, doc) \
		ob = Py_InitModule3(name, NULL, doc);
#endif

MOD_INIT(reference) {
	PyObject *m;
	
	MOD_DEF(m, "_reference", "Atomic reference module");
	if (m == NULL) {
		return MOD_ERROR_VAL;
	}
	
	ReferenceType.tp_new = PyType_GenericNew;	
	if (PyType_Ready(&ReferenceType) < 0) {
		return MOD_ERROR_VAL;
	}
	
	Py_INCREF(&ReferenceType);
	PyModule_AddObject(m, "Reference", (PyObject *)&ReferenceType);
	
	return MOD_SUCCESS_VAL(m);
}