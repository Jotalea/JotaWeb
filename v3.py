from PyQt5.QtCore import Qt, QObject, pyqtSlot, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
import sys

initial_url = "http://jotalea.com.ar"

class ConsoleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Console")
        self.console_output = QPlainTextEdit()
        self.console_output.setReadOnly(True)
        self.setCentralWidget(self.console_output)

    def write(self, text):
        self.console_output.insertPlainText(text)

class JotaleaWebBrowser(QMainWindow):
    class Bridge(QObject):
        @pyqtSlot(str)
        def jotaleaprint(self):
            print("--------------------Hello--------------------")

    def __init__(self):
        super(JotaleaWebBrowser, self).__init__()
        self.window = QWidget()
        self.window.setWindowTitle("Jotalea Web Browser")

        self.showMaximized()

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.bar_url = QTextEdit()
        self.bar_url.setMaximumHeight(30)
        self.bar_url.textChanged.connect(self.limitURLBar)

        self.btn_go = QPushButton("➔")
        self.btn_go.setMinimumHeight(30)
        self.btn_go.setMaximumWidth(30)

        self.btn_refresh = QPushButton("⟳")
        self.btn_refresh.setMinimumHeight(30)
        self.btn_refresh.setMaximumWidth(30)

        self.btn_back = QPushButton("◄")
        self.btn_back.setMinimumHeight(30)
        self.btn_back.setMaximumWidth(30)

        self.btn_forward = QPushButton("►")
        self.btn_forward.setMinimumHeight(30)
        self.btn_forward.setMaximumWidth(30)

        self.btn_console = QPushButton("Console")
        self.btn_console.setMinimumHeight(30)

        #self.horizontal.addWidget(self.bar_url)
        #self.horizontal.addWidget(self.btn_go)
        #self.horizontal.addWidget(self.btn_refresh)
        #self.horizontal.addWidget(self.btn_back)
        #self.horizontal.addWidget(self.btn_forward)
        #self.horizontal.addWidget(self.btn_console)

        self.navbar.addWidget(self.bar_url)
        self.navbar.addWidget(self.btn_go)
        self.navbar.addWidget(self.btn_refresh)
        self.navbar.addWidget(self.btn_back)
        self.navbar.addWidget(self.btn_forward)
        #self.navbar.addWidget(self.btn_console)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        #self.navbar.addWidget(self.url_bar)

        self.browser = QWebEngineView()

        self.btn_go.clicked.connect(lambda: self.navigate(self.bar_url.toPlainText()))
        self.btn_refresh.clicked.connect(lambda: self.browser.reload())
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)
        self.btn_console.clicked.connect(self.show_console)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl(initial_url))
        self.bar_url.setText(initial_url)

        self.channel = QWebChannel()
        self.bridge = self.Bridge()
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        self.browser.urlChanged.connect(self.updateURLBar)
        self.browser.titleChanged.connect(self.updateWindowTitle)

        self.window.setLayout(self.layout)
        self.window.show()

    def show_console(self):
        sys.stdout = self.console
        sys.stderr = self.console
        self.console_window.show()

    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            if "." in url and " " not in url:
                url = "http://" + url
                self.bar_url.setText(url)
                self.browser.setUrl(QUrl(url))
            else:
                url = "https://duckduckgo.com/?q=" + url
                self.bar_url.setText(url)
                self.browser.setUrl(QUrl(url))
                return
        else:
            self.browser.setUrl(QUrl(url))

    def limitURLBar(self):
        text = self.bar_url.toPlainText()
        if '\n' in text:
            lines = text.split('\n')
            self.bar_url.setPlainText(lines[0])
            url = self.bar_url.toPlainText()
            if not url.startswith("http"):
                if "." in url and " " not in url:
                    url = "http://" + url
                    self.bar_url.setText(url)
                    self.browser.setUrl(QUrl(url))
                else:
                    url = "https://duckduckgo.com/?q=" + url
                    self.bar_url.setText(url)
                    self.browser.setUrl(QUrl(url))
                    return
            else:
                self.browser.setUrl(QUrl(url))

    def updateURLBar(self, url):
        self.bar_url.setText(url.toString())

    def updateWindowTitle(self, title):
        self.window.setWindowTitle(f"{title} - Jotalea Web Browser")

class JotaleaWebBrowserError(QMainWindow):
    def __init__(self, error_message):
        super().__init__()
        self.setWindowTitle("Error")
        self.error_message = error_message
        self.error_text_edit = QTextEdit()
        self.error_text_edit.setPlainText(self.error_message)
        self.setCentralWidget(self.error_text_edit)

if __name__ == "__main__":
    app = QApplication([])

    if True:
        try:
            browser_window = JotaleaWebBrowser()
            console_window = ConsoleWindow()
            browser_window.console = console_window
            app.exec_()
        except Exception as e:
            print(str(e))
            error_message = str(e)
            error_window = JotaleaWebBrowserError(error_message)
            error_window.show()
            app.exec_()