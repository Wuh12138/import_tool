import sys
import time
import urllib.request
import json
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QStringListModel, QUrl, QObject, Slot, QEventLoop, QTimer
from PySide6.QtGui import QGuiApplication

from execute import Execute

Instance = Execute()


class PageManager:
    def __init__(self):
        self.page_list = []

    def goBack(self):
        if len(self.page_list) != 1:
            self.page_list.pop().close()
            self.page_list[-1].show()
        elif len(self.page_list) == 1:
            self.page_list.pop().close()

    def goNext(self, page):
        if len(self.page_list) != 0:
            self.page_list[-1].hide()
            self.page_list.append(page)
            self.page_list[-1].show()
        elif len(self.page_list) == 0:
            self.page_list.append(page)
            self.page_list[-1].show()


pageManager = PageManager()


class CommonInterface(QObject):
    @Slot(str, result=str)
    def FormatFilePath(self, path: str) -> str:
        return path.replace("file:///", "")

    @Slot(str)
    def PLog(self, message: str):
        print(message)

    @staticmethod
    def errorLog(message: str):
        error_dialog = QQuickView()
        error_dialog.setTitle("error")
        error_dialog.rootContext().setContextProperty("error_message", message)

        error_dialog.setSource(QUrl.fromLocalFile(str(Path(__file__).parent / f"qml/ErrorDialog.qml")))
        if error_dialog.status() == QQuickView.Error:
            print(error_dialog.errors())
            sys.exit(-1)

        error_dialog.show()
        loop = QEventLoop()

        loop.exec()


class Page1(QObject):

    def __init__(self, qmlPath: str = "qml/Page1.qml"):
        super().__init__()
        self.qml_path = Path(__file__).parent / f"{qmlPath}"
        self.view = QQuickView()
        self.view.setTitle("登陆")

        # register python class to qml
        self.view.rootContext().setContextProperty("Page1_I", self)
        self.common_interface = CommonInterface()
        self.view.rootContext().setContextProperty("CIN", self.common_interface)

        self.view.setSource(QUrl.fromLocalFile(str(self.qml_path)))
        if self.view.status() == QQuickView.Error:
            print(self.view.errors())
            sys.exit(-1)

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def hide(self):
        self.view.setProperty("visible", False)

    @Slot(str, str, str, str, str)
    def submit(self, neo4j_url: str, neo4j_user: str, neo4j_password: str, neo4j_database: str, xmind_path: str):
        xmind_path = xmind_path.replace("file:///", "")
        print(neo4j_url, neo4j_user, neo4j_password, neo4j_database, xmind_path)
        # try:
        #     Instance.set_neo4j(neo4j_password, neo4j_user, neo4j_url)
        #     Instance.parse_xmind(xmind_path)
        # except Exception as e:
        #     CommonInterface.errorLog(str(e))
        #     return

        pageManager.goNext(Page2())


class Page2(QObject):

    def __init__(self, qmlPath: str = "qml/Page2.qml"):
        super().__init__()
        self.qml_path = Path(__file__).parent / f"{qmlPath}"
        self.view = QQuickView()
        self.view.setTitle("选择源数据库")

        # register python class to qml
        self.view.rootContext().setContextProperty("Page2_I", self)
        self.common_interface = CommonInterface()
        self.view.rootContext().setContextProperty("CIN", self.common_interface)

        self.view.setSource(QUrl.fromLocalFile(str(self.qml_path)))
        if self.view.status() == QQuickView.Error:
            print(self.view.errors())
            sys.exit(-1)

    def show(self):
        self.view.show()

    def close(self):
        self.view.close()

    def hide(self):
        self.view.setProperty("visible", False)

    @Slot()
    def goBack(self):
        pageManager.goBack()

    @Slot(str)
    def submit(self, args: str):
        print(args)

        args_list = args.split(" ")
        if args_list[0] == "mysql":
            Instance.set_source("mysql", host=args_list[1], user=args_list[2], password=args_list[3],
                                database=args_list[4])
        elif args_list[0] == "xlsx":
            Instance.set_source("xlsx", xlsx_path=args_list[1])
        else:
            raise Exception("wait to be completed")

class Page3(QObject):
    def __init__(self, qmlPath: str = "qml/Page3.qml"):
        super().__init__()
        self.qml_path = Path(__file__).parent / f"{qmlPath}"
        self.view = QQuickView()
        self.view.setTitle("数据导入")

        # register python class to qml
        self.view.rootContext().setContextProperty("Page3_I", self)
        self.common_interface = CommonInterface()
        self.view.rootContext().setContextProperty("CIN", self.common_interface)

        self.view.setSource(QUrl.fromLocalFile(str(self.qml_path)))
        if self.view.status() == QQuickView.Error:
            print(self.view.errors())
            sys.exit(-1)






if __name__ == '__main__':
    # Set up the application window
    app = QGuiApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    pageManager.goNext(Page1())
    app.exec()
