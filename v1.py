from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget

initial_url = "http://jotalea.com.ar"

class JotaleaWebBrowser():

    def __init__(self):

        self.window = QWidget()
        self.window.setWindowTitle("Jotalea Web Browser")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.bar_url = QTextEdit()
        self.bar_url.setMaximumHeight(30)
        self.bar_url.textChanged.connect(self.limitURLBar)

        self.btn_go = QPushButton("Go")
        self.btn_go.setMinimumHeight(30)

        self.btn_back = QPushButton("<")
        self.btn_back.setMinimumHeight(30)

        self.btn_forward = QPushButton(">")
        self.btn_forward.setMinimumHeight(30)

        self.horizontal.addWidget(self.bar_url)
        self.horizontal.addWidget(self.btn_go)
        self.horizontal.addWidget(self.btn_back)
        self.horizontal.addWidget(self.btn_forward)

        self.browser = QWebEngineView()

        self.btn_go.clicked.connect(lambda: self.navigate(self.bar_url.toPlainText()))
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl(initial_url))
        self.bar_url.setText(initial_url)

        self.browser.urlChanged.connect(self.updateURLBar)
        self.browser.titleChanged.connect(self.updateWindowTitle)

        self.window.setLayout(self.layout)
        self.window.show()

    def navigate(self, url):
        if not url.startswith("http"): # Two options: it is a website wrongly written, or a search
            if "." in str(url) and not " " in str(url):
                url = "http://" + url
                self.bar_url.setText(url)
                self.browser.setUrl(QUrl(url))
            else:
                self.bar_url.setText("https://duckduckgo.com/?q=" + url)
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
                url = "http://" + url
                self.bar_url.setText(url)
            self.browser.setUrl(QUrl(url))

    def updateURLBar(self, url):
        self.bar_url.setText(url.toString())

    def updateWindowTitle(self, title):
        self.window.setWindowTitle(title)

app = QApplication([])
window = JotaleaWebBrowser()
exit(app.exec_())
