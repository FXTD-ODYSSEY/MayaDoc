import os
import importlib
from urllib import request

DIR, FILE = os.path.split(__file__)

MODULE = os.path.join(DIR, "PySide2")
WEB = r"https://doc.qt.io/qtforpython/"


def downloadHTML():

    unavailable_list = {
        "QtCore": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "ClassInfo",
            "_Object",
            "QtMsgType",
            "MetaFunction",
            "Signal",
            "Slot",
            "Property",
            "Connection",
            "QWinEventNotifier",
            "qIsInf",
            "SIGNAL",
            "qAcos",
            "qAtan2",
            "qExp",
            "qFatal",
            "qIsFinite",
            "QT_TRANSLATE_NOOP",
            "qRegisterResourceData",
            "QT_TRANSLATE_NOOP3",
            "qAbs",
            "qAtan",
            "qDebug",
            "qFastSin",
            "qInstallMessageHandler",
            "QT_TRANSLATE_NOOP_UTF8",
            "qIsNull",
            "qAddPostRoutine",
            "qVersion",
            "__moduleShutdown",
            "qWarning",
            "QT_TR_NOOP",
            "qAsin",
            "qCritical",
            "qFuzzyIsNull",
            "QT_TR_NOOP_UTF8",
            "qIsNaN",
            "qUnregisterResourceData",
            "qFastCos",
            "qsrand",
            "qtTrId",
            "qChecksum",
            "qFuzzyCompare",
            "SLOT",
            "qFabs",
            "qTan",
            "qrand",
            "QtDebugMsg",
            "QtWarningMsg",
            "QtCriticalMsg",
            "QtFatalMsg",
            "QtInfoMsg",
            "QtSystemMsg",
            "__version__"
        ],
        "QtGui": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QEvent",
            "_QAbstractListModel",
            "_QCoreApplication",
            "_QObject",
            "_QAbstractItemModel",
            "_Object",
            "QStringListModel",
            "QPyTextObject",
            "qAlpha",
            "qGreen",
            "qRed",
            "qIsGray",
            "qGray",
            "qRgb",
            "qRgba",
            "qBlue"
        ],
        "QtHelp": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_QStringListModel",
            "_QAbstractItemModel",
            "_QWidget",
            "_QTreeView",
            "_QListView",
            "_Object"
        ],
        "QtMultimedia": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_Object"
        ],
        "QtNetwork": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QIODevice",
            "_QObject",
            "_Object"
        ],
        "QtOpenGL": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWidget",
            "_QPaintDevice",
            "_QObject",
            "_Object",
            "QGLFramebufferObjectFormat"
        ],
        "QtPrintSupport": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWidget",
            "_QPagedPaintDevice",
            "_QDialog",
            "_Object"
        ],
        "QtQml": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_Object",
            "VolatileBool",
            "_Property",
            "ListProperty",
            "qmlRegisterType",
            "QML_HAS_ATTACHED_PROPERTIES"
        ],
        "QtQuick": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWindow",
            "_QQmlImageProviderBase",
            "_QObject",
            "_QQmlParserStatus",
            "_Object"
        ],
        "QtQuickWidgets": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWidget"
        ],
        "QtScript": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_QFactoryInterface",
            "_Object",
            "QScriptExtensionInterface",
            "QScriptValue",
            "QScriptContext",
            "QScriptEngineAgent",
            "QScriptEngine",
            "QScriptable",
            "QScriptProgram",
            "QScriptClassPropertyIterator",
            "QScriptClass",
            "QScriptContextInfo",
            "QScriptString",
            "QScriptValueIterator",
            "QScriptExtensionPlugin"
        ],
        "QtSql": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_QAbstractTableModel",
            "_QItemDelegate",
            "_Object",
            "QSqlRelationalDelegate"
        ],
        "QtSvg": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWidget",
            "_QGraphicsObject",
            "_QObject",
            "_QPaintDevice"
        ],
        "QtTest": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_Object"
        ],
        "QtUiTools": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject"
        ],
        "QtWebChannel": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject"
        ],
        "QtWebKit": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_Object",
            "WebCore"
        ],
        "QtWebKitWidgets": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QWidget",
            "_QGraphicsWidget",
            "_QObject",
            "_Object",
            "QWebPluginFactory",
            "QWebView",
            "QWebElementCollection",
            "QWebHistory",
            "QWebHistoryInterface",
            "QWebElement",
            "QGraphicsWebView",
            "QWebPage",
            "QWebHistoryItem",
            "QWebHitTestResult",
            "QWebSecurityOrigin",
            "QWebDatabase",
            "QWebFrame",
            "QWebSettings",
            "QWebInspector"
        ],
        "QtWebSockets": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_Object"
        ],
        "QtWidgets": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QPainter",
            "_QAbstractTextDocumentLayout",
            "_QEvent",
            "_QEventTransition",
            "_QGuiApplication",
            "_QPaintDevice",
            "_QObject",
            "_QAbstractItemModel",
            "_Object",
            "QAction",
            "qApp"
        ],
        "QtXml": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_Object"
        ],
        "QtXmlPatterns": [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__file__",
            "__cached__",
            "__builtins__",
            "_QObject",
            "_Object"
        ]
    }

    unavailable_list = {}
    for i, module in enumerate(os.listdir(MODULE)):
        if not module.startswith("Qt"):
            continue

        module_name = os.path.splitext(module)[0]
        module = importlib.import_module(f"PySide2.{module_name}")

        unavailable_list[module_name] = []
        for j, class_name in enumerate(module.__dict__):
            
            if class_name in unavailable_list[module_name]:
                continue

            target = f"{module_name}/{class_name}.html"
            url = f"{WEB}PySide2/{target}"

            # NOTE 如果是404记录下来并跳过
            try:
                req = request.urlopen(url)
            except:
                unavailable_list[module_name].append(class_name)
                continue

            print(i, j, class_name)

            content = req.read()
            HTML = os.path.join(DIR, "HTML", target)
            FOLDER = os.path.dirname(HTML)
            if not os.path.exists(FOLDER):
                os.makedirs(FOLDER)

            with open(HTML, 'wb') as f:
                f.write(content)

if __name__ == "__main__":
    downloadHTML()
