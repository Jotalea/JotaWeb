from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

initial_url = "http://jotalea.com.ar"

class JotaleaWebBrowser():
    class Bridge(QObject):
        @pyqtSlot(str)
        def jotaleaprint(self):
            print("--------------------Hello--------------------")

    def __init__(self):
        super(JotaleaWebBrowser, self).__init__()
        self.window = QWidget()
        self.window.setWindowTitle("JotaWeb")

        self.window.showMaximized()

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

        self.horizontal.addWidget(self.bar_url)
        self.horizontal.addWidget(self.btn_go)
        self.horizontal.addWidget(self.btn_refresh)
        self.horizontal.addWidget(self.btn_back)
        self.horizontal.addWidget(self.btn_forward)

        self.browser = QWebEngineView()

        self.btn_go.clicked.connect(lambda: self.navigate(self.bar_url.toPlainText()))
        self.btn_refresh.clicked.connect(lambda: self.browser.reload())
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)

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

    def navigate(self, url):
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
        self.window.setWindowTitle(f"{title} | JotaWeb")

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
    try:
        browser_window = JotaleaWebBrowser()
        app.exec_()
    except Exception as e:
        print(str(e))
        error_message = str(e)
        error_window = JotaleaWebBrowserError(error_message)
        error_window.show()
        app.exec_()