import re
import json
import os
import importlib
from collections import OrderedDict
from html2text import HTML2Text
from bs4 import BeautifulSoup, NavigableString

parser = HTML2Text()
# parser.wrap_links = False
# parser.inline_links = True
parser.skip_internal_links = True
parser.ignore_anchors = True
parser.ignore_images = True
parser.ignore_emphasis = True
parser.ignore_table = True
parser.ignore_links = True

DIR, FILE = os.path.split(__file__)

MODULE = os.path.join(DIR, "PySide2")
HTML = os.path.join(DIR, "HTML")
WEB = r"https://doc.qt.io/qtforpython/"

def main():

    PySide_dict = {}

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
    for i, module in enumerate(os.listdir(MODULE)):
        if not module.startswith("Qt"):
            continue

        module_name = os.path.splitext(module)[0]
        module = importlib.import_module(f"PySide2.{module_name}")

        PySide_dict[module_name] = {}
        for j, class_name in enumerate(module.__dict__):
            if class_name in unavailable_list[module_name]:
                continue
            
            target = f"{module_name}/{class_name}.html"

            html = f"{HTML}/{target}"

            with open(html,'r',encoding="utf-8") as f:
                content = f.read()
            
            # NOTE 提取类描述
            soup = BeautifulSoup(content, 'html.parser')
            
            # TODO 测试
            # if len(soup.findAll('dl', {"class": "class"})) > 1:
            #     print ("class",html)
            # elif len(soup.findAll('blockquote', id="more")) > 1:
            #     print("blockquote", html)

            if j < 15:
                continue
            if j > 16:
                break
            print(j, class_name)

            # NOTE 清除 seealso 关联
            for seealso in soup.findAll('div', {"class": "admonition seealso"}):
                seealso.decompose()

            class_description = soup.find('blockquote')
            class_description = parser.handle(str(class_description.div)).strip()
            class_description,_ = class_description.replace("\n", " ").split("More")

            # TODO
            # class_detail_description 

            # NOTE 提取构造函数
            constructor_dict = {}
            constructor = soup.find('dl', {"class": "class"})
            # print(str(constructor))

            # NOTE 提取 头部 函数信息
            header = constructor.findChild('dt', id=f"{module.__name__}.{class_name}").extract()
            param = constructor.findChild('blockquote').extract()

            func_list = [re.search('class (.*?¶)', header.text.strip()).group(1)]
            for func in param.findChild('blockquote').extract().findAll('p'):
                func_list.append(func.text)
            
            param_list = []
            for dt,dd in zip(param.findAll('dt'),param.findAll('dd')):
                dt = parser.handle(str(dt)).strip()
                dd = parser.handle(str(dd)).strip()
                param_list.append(f'{dt.split(" ")[-1]:<20}{dd}')

            for note in constructor.findAll('div', {"class": "admonition note"}):
                note.find('p', {"class": "admonition-title"}).decompose()
                replace_text = "> %s" % parser.handle(str(note.p))
                note.p.replaceWith(replace_text)
                
            instruction = parser.handle(str(constructor)).strip()

            constructor_dict["func"] = func_list
            constructor_dict["param_list"] = param_list
            constructor_dict["instruction"] = instruction

            attribute_list = []
            for attribute in soup.findAll('dl', {"class": "attribute"}):
                attr_name = attribute.dt.text.strip()
                description = parser.handle(str(attribute.dd.p))
                flag_list = []
                for attr in attribute.table.tbody.findAll("tr"):
                    for _i,data in enumerate(attr.findAll("td")):
                        if _i % 2 :
                            # NOTE 奇数
                            instruction += "    %s" % data.text
                            flag_list.append(instruction)
                        else:
                            # NOTE 偶数 
                            instruction = "%-20s" % data.text

                attribute_list.append({
                    "attr_name": attr_name,
                    "description": description,
                    "flag_list": flag_list,
                })
                

            method_list = []
            for method in soup.findAll('dl', {"class": "method"}):
                method_name = method.dt.text.strip()
                returns = parser.handle(str(method.dd.dl.extract().dd)).strip()
                description = parser.handle(str(method.dd)).strip()

                method_list.append({
                    "method_name": re.search(f'{class_name}\.(.*?)\(.*?¶', method_name).group(1),
                    "method_long_name": method_name,
                    "description": description,
                    "returns": returns,
                })
                    


            PySide_dict[module_name][class_name] = {
                "description": class_description,
                "link":f"{WEB}PySide2/{target}",
                "constructor": constructor_dict,
                "attribute": attribute_list,
                "method": method_list,
            }

            
        break
    
    # print (json.dumps(PySide_dict))
    JSON = os.path.join(DIR, "PySide2.json")
    with open(JSON,'w') as f:
        json.dump(PySide_dict, f, indent=4)


if __name__ == "__main__":
    main()
