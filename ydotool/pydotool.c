#include "pydotool.h"

#define MODULE_STATE(o) ((modulestate *) PyModule_GetState(o))


PyObject *pydotool_init(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *pydotool_uinput_emit(PyObject *self, PyObject *args, PyObject *kwargs);


static PyMethodDef pydotool_Methods[] = {
        {"init", (PyCFunction) pydotool_init, METH_VARARGS | METH_KEYWORDS, "Initialize ydotool."},
        {"uinput_emit", (PyCFunction) pydotool_uinput_emit, METH_VARARGS | METH_KEYWORDS, "Emit input event."},
        {NULL, NULL, 0, NULL} /* Sentinel */
};

static int module_traverse(PyObject *m, visitproc visit, void *arg);
static int module_clear(PyObject *m);
static void module_free(void *m);
typedef struct
{
    PyObject *type_decimal;
} modulestate;

static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_pydotool",
        0,                   /* m_doc */
        sizeof(modulestate), /* m_size */
        pydotool_Methods,    /* m_methods */
        NULL,                /* m_slots */
        module_traverse,     /* m_traverse */
        module_clear,        /* m_clear */
        module_free          /* m_free */
};

static int module_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(MODULE_STATE(m)->type_decimal);
    return 0;
}

static int module_clear(PyObject *m) {
    Py_CLEAR(MODULE_STATE(m)->type_decimal);
    return 0;
}

static void module_free(void *m) {
    module_clear((PyObject *) m);
}


PyMODINIT_FUNC PyInit__pydotool(void) {
    PyObject *module;


    // This function is not supported in PyPy.
    if ((module = PyState_FindModule(&moduledef)) != NULL) {
        Py_INCREF(module);
        return module;
    }


    module = PyModule_Create(&moduledef);
    if (module == NULL) {
        return NULL;
    }

    PyModule_AddStringConstant(module, "__version__", VERSION);

    return module;
}

PyObject *pydotool_init(PyObject *self, PyObject *args, PyObject *kwargs) {
    char *env_ys = NULL;
    static const char *kwlist[] = {"socket_path", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|s#", (char **) kwlist, &env_ys)) {
        PyErr_SetString(PyExc_TypeError, "_pydotool.init(): failed to parse argument, expecting string");
        return NULL;
    }

    if (env_ys == NULL) env_ys = getenv("YDOTOOL_SOCKET");
    if (env_ys == NULL) {
        env_ys = "/tmp/.ydotool_socket";
    }

    if (fd_daemon_socket < 0) {
        fd_daemon_socket = socket(AF_UNIX, SOCK_DGRAM, 0);
    }

    if (fd_daemon_socket < 0) {
        PyErr_SetString(PyExc_RuntimeError, "failed to create socket");
        return NULL;
    }

    struct sockaddr_un sa = {
            .sun_family = AF_UNIX,
    };

    snprintf(sa.sun_path, sizeof(sa.sun_path) - 1, "%s", env_ys);

    if (connect(fd_daemon_socket, (const struct sockaddr *) &sa, sizeof(sa))) {
        int err = errno;
        printf("failed to connect socket `%s': %s\n", sa.sun_path, strerror(err));

        switch (err) {
            case ENOENT:
            case ECONNREFUSED:
                PyErr_SetString(PyExc_RuntimeError, "Please check if ydotoold is running.");
                break;
            case EACCES:
            case EPERM:
                PyErr_SetString(PyExc_RuntimeError, "Please check if the current user has sufficient permissions to access the socket file.");
                break;
        }

        return NULL;
    }
    Py_RETURN_NONE;
}

PyObject *pydotool_uinput_emit(PyObject *self, PyObject *args, PyObject *kwargs) {
    // uint16_t type, uint16_t code, int32_t val, bool syn_report
    if (fd_daemon_socket < 0) {
        PyErr_SetString(PyExc_RuntimeError, "socket is not initialized, call init() first");
        return NULL;
    }
    unsigned short type, pad1, code, pad2;
    assert(sizeof(unsigned short) == 2);
    int32_t pad3;
    int32_t val;
    int32_t syn_report;
    static const char *kwlist[] = {"type", "code", "val", "syn_report", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "HHip", (char **) kwlist, &type, &code, &val, &syn_report)) {
        PyErr_SetString(PyExc_TypeError, "_pydotool.uinput_emit(): failed to parse argument");
        return NULL;
    }
    uinput_emit(type, code, val, (bool) syn_report);
    Py_RETURN_NONE;
}
