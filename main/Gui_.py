import sys
import urllib.request
import json
from pathlib import Path

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QStringListModel, QUrl, QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFileDialog


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
            self.page_list[-1].close()
            self.page_list.append(page)
            self.page_list[-1].show()
        elif len(self.page_list) == 0:
            self.page_list.append(page)
            self.page_list[-1].show()


pageManager = PageManager()


class Page1(QObject):

    def __init__(self, qmlPath: str = "qml/Page1.qml"):
        super().__init__()
        self.qml_path = Path(__file__).parent / f"{qmlPath}"
        self.engine = QQuickView()
        self.engine.setTitle("登陆")

        # register python class to qml
        self.engine.rootContext().setContextProperty("Page1_I", self)

        self.engine.setSource(QUrl.fromLocalFile(str(self.qml_path)))
        if self.engine.status() == QQuickView.Error:
            print(self.engine.errors())
            sys.exit(-1)

    def show(self):
        self.engine.show()

    def close(self):
        self.engine.close()

    @Slot(str, str, str, str, str)
    def submit(self, neo4j_url: str, neo4j_user: str, neo4j_password: str, neo4j_database: str, xmind_path: str):
        xmind_path = xmind_path.replace("file:///", "")
        print(neo4j_url, neo4j_user, neo4j_password, neo4j_database, xmind_path)
        # TODO:

        pageManager.goNext(Page2())


class Page2(QObject):

    def __init__(self, qmlPath: str = "qml/Page2.qml"):
        super().__init__()
        self.qml_path = Path(__file__).parent / f"{qmlPath}"
        self.engine = QQuickView()
        self.engine.setTitle("选择源数据库")

        # register python class to qml
        self.engine.rootContext().setContextProperty("Page2_I", self)

        self.engine.setSource(QUrl.fromLocalFile(str(self.qml_path)))
        if self.engine.status() == QQuickView.Error:
            print(self.engine.errors())
            sys.exit(-1)

    def show(self):
        self.engine.show()

    def close(self):
        self.engine.close()


if __name__ == '__main__':
    # Set up the application window
    app = QGuiApplication(sys.argv)

    window = Page1()
    pageManager.goNext(window)

    app.exec()
