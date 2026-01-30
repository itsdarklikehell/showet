/****************************************************************************
** Meta object code from reading C++ file 'showethelper.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.10)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "showethelper.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'showethelper.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.10. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_ShowetHelper_t {
    QByteArrayData data[20];
    char stringdata0[249];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_ShowetHelper_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_ShowetHelper_t qt_meta_stringdata_ShowetHelper = {
    {
QT_MOC_LITERAL(0, 0, 12), // "ShowetHelper"
QT_MOC_LITERAL(1, 13, 8), // "runError"
QT_MOC_LITERAL(2, 22, 0), // ""
QT_MOC_LITERAL(3, 23, 9), // "errorText"
QT_MOC_LITERAL(4, 33, 14), // "runningChanged"
QT_MOC_LITERAL(5, 48, 7), // "running"
QT_MOC_LITERAL(6, 56, 25), // "supportedPlatformsChanged"
QT_MOC_LITERAL(7, 82, 15), // "processFinished"
QT_MOC_LITERAL(8, 98, 8), // "exitCode"
QT_MOC_LITERAL(9, 107, 20), // "QProcess::ExitStatus"
QT_MOC_LITERAL(10, 128, 10), // "exitStatus"
QT_MOC_LITERAL(11, 139, 20), // "processErrorOccurred"
QT_MOC_LITERAL(12, 160, 22), // "QProcess::ProcessError"
QT_MOC_LITERAL(13, 183, 5), // "error"
QT_MOC_LITERAL(14, 189, 13), // "printRunError"
QT_MOC_LITERAL(15, 203, 7), // "runDemo"
QT_MOC_LITERAL(16, 211, 2), // "id"
QT_MOC_LITERAL(17, 214, 10), // "cancelDemo"
QT_MOC_LITERAL(18, 225, 4), // "init"
QT_MOC_LITERAL(19, 230, 18) // "supportedPlatforms"

    },
    "ShowetHelper\0runError\0\0errorText\0"
    "runningChanged\0running\0supportedPlatformsChanged\0"
    "processFinished\0exitCode\0QProcess::ExitStatus\0"
    "exitStatus\0processErrorOccurred\0"
    "QProcess::ProcessError\0error\0printRunError\0"
    "runDemo\0id\0cancelDemo\0init\0"
    "supportedPlatforms"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_ShowetHelper[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       2,   82, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       3,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   59,    2, 0x06 /* Public */,
       4,    1,   62,    2, 0x06 /* Public */,
       6,    0,   65,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       7,    2,   66,    2, 0x08 /* Private */,
      11,    1,   71,    2, 0x08 /* Private */,
      14,    1,   74,    2, 0x08 /* Private */,

 // methods: name, argc, parameters, tag, flags
      15,    1,   77,    2, 0x02 /* Public */,
      17,    0,   80,    2, 0x02 /* Public */,
      18,    0,   81,    2, 0x02 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, QMetaType::Bool,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::Int, 0x80000000 | 9,    8,   10,
    QMetaType::Void, 0x80000000 | 12,   13,
    QMetaType::Void, QMetaType::QString,    3,

 // methods: parameters
    QMetaType::Void, QMetaType::UInt,   16,
    QMetaType::Void,
    QMetaType::Void,

 // properties: name, type, flags
       5, QMetaType::Bool, 0x00495003,
      19, QMetaType::QStringList, 0x00495003,

 // properties: notify_signal_id
       1,
       2,

       0        // eod
};

void ShowetHelper::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<ShowetHelper *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->runError((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 1: _t->runningChanged((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: _t->supportedPlatformsChanged(); break;
        case 3: _t->processFinished((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QProcess::ExitStatus(*)>(_a[2]))); break;
        case 4: _t->processErrorOccurred((*reinterpret_cast< QProcess::ProcessError(*)>(_a[1]))); break;
        case 5: _t->printRunError((*reinterpret_cast< QString(*)>(_a[1]))); break;
        case 6: _t->runDemo((*reinterpret_cast< const uint(*)>(_a[1]))); break;
        case 7: _t->cancelDemo(); break;
        case 8: _t->init(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (ShowetHelper::*)(QString );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ShowetHelper::runError)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (ShowetHelper::*)(bool );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ShowetHelper::runningChanged)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (ShowetHelper::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ShowetHelper::supportedPlatformsChanged)) {
                *result = 2;
                return;
            }
        }
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty) {
        auto *_t = static_cast<ShowetHelper *>(_o);
        (void)_t;
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< bool*>(_v) = _t->m_running; break;
        case 1: *reinterpret_cast< QStringList*>(_v) = _t->m_supportedPlatforms; break;
        default: break;
        }
    } else if (_c == QMetaObject::WriteProperty) {
        auto *_t = static_cast<ShowetHelper *>(_o);
        (void)_t;
        void *_v = _a[0];
        switch (_id) {
        case 0:
            if (_t->m_running != *reinterpret_cast< bool*>(_v)) {
                _t->m_running = *reinterpret_cast< bool*>(_v);
                Q_EMIT _t->runningChanged(_t->m_running);
            }
            break;
        case 1:
            if (_t->m_supportedPlatforms != *reinterpret_cast< QStringList*>(_v)) {
                _t->m_supportedPlatforms = *reinterpret_cast< QStringList*>(_v);
                Q_EMIT _t->supportedPlatformsChanged();
            }
            break;
        default: break;
        }
    } else if (_c == QMetaObject::ResetProperty) {
    }
#endif // QT_NO_PROPERTIES
}

QT_INIT_METAOBJECT const QMetaObject ShowetHelper::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_ShowetHelper.data,
    qt_meta_data_ShowetHelper,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *ShowetHelper::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ShowetHelper::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_ShowetHelper.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int ShowetHelper::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 9;
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 2;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 2;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 2;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 2;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 2;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 2;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void ShowetHelper::runError(QString _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void ShowetHelper::runningChanged(bool _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void ShowetHelper::supportedPlatformsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 2, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
