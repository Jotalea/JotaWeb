from PyQt5.QtCore import Qt, QObject, pyqtSlot, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWidgets import QWidget, QToolBar
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

initial_url = "http://start.jotalea.com.ar"

"""
<!DOCTYPE html>
<html>
    <head>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    </head>
    <body>
        <script>
            var backend;
            new QWebChannel(qt.webChannelTransport, function (channel) {
                backend = channel.objects.backend;
            });

            backend.myfunction();
        </script>
    </body>
</html>
"""

class JotaleaWebBrowser(QMainWindow):
    class Bridge(QObject):
        @pyqtSlot(str)
        def jotaleaprint(self, message):
            print("--------------------", message, "--------------------")

    def __init__(self):
        super(JotaleaWebBrowser, self).__init__()
        self.setWindowTitle("JotaWeb")

        self.setGeometry(
            int(int(QGuiApplication.primaryScreen().geometry().width()) / 2 - 360),     # Screen width
            int(int(QGuiApplication.primaryScreen().geometry().height()) / 2 - 240),    # Screen height
            720,                                                                        # Window width
            480                                                                         # Window height
        )
        self.setMinimumSize(360, 360)

        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.bar_url = QTextEdit()
        self.bar_url.setMaximumHeight(30)
        self.bar_url.textChanged.connect(self.limitURLBar)  #self.bar_url.returnPressed.connect(self.limitURLBar)

        self.btn_go = QPushButton("➔")
        self.btn_go.setFixedHeight(30)
        self.btn_go.setMaximumWidth(30)

        self.btn_refresh = QPushButton("⟳")
        self.btn_refresh.setFixedHeight(30)
        self.btn_refresh.setMaximumWidth(30)

        self.btn_back = QPushButton("◄")
        self.btn_back.setFixedHeight(30)
        self.btn_back.setMaximumWidth(30)

        self.btn_forward = QPushButton("►")
        self.btn_forward.setFixedHeight(30)
        self.btn_forward.setMaximumWidth(30)

        self.navbar = CustomToolBar()
        self.addToolBar(self.navbar)

        self.navbar.addWidget(self.bar_url)
        self.navbar.addWidget(self.btn_go)
        self.navbar.addWidget(self.btn_refresh)
        self.navbar.addWidget(self.btn_back)
        self.navbar.addWidget(self.btn_forward)

        self.browser = QWebEngineView()
        self.browser.setMinimumHeight(360)
        self.browser.setMinimumWidth(360)

        self.layout.addWidget(self.browser)

        self.browser.setUrl(QUrl(initial_url))
        self.bar_url.setText(initial_url)

        self.channel = QWebChannel()
        self.bridge = self.Bridge()
        self.channel.registerObject("bridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        self.browser.urlChanged.connect(self.updateURLBar)
        self.browser.titleChanged.connect(self.updateWindowTitle)

        self.btn_go.clicked.connect(self.navigate)
        self.btn_refresh.clicked.connect(self.browser.reload)
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)

        self.setCentralWidget(self.widget)
        self.show()

    def navigate(self):
        try:
            url = self.bar_url.toPlainText()
        except AttributeError:
            url = self.bar_url.text()
        
        if not url.startswith("http"):
            if "." in url and " " not in url:
                url = "http://" + url
            else:
                url = "https://duckduckgo.com/?q=" + url
        self.browser.setUrl(QUrl(url))
        self.bar_url.clearFocus()

    def limitURLBar(self):
        try:
            text = self.bar_url.toPlainText()
        except AttributeError:
            text = self.bar_url.text()
        
        if '\n' in text:
            lines = text.split('\n')
            self.bar_url.setPlainText(lines[0])

            try:
                url = self.bar_url.toPlainText()
            except AttributeError:
                url = self.bar_url.text()

            if not url.startswith("http"):
                if "." in url and " " not in url:
                    url = "http://" + url
                    self.bar_url.setText(url)
                    self.browser.setUrl(QUrl(url))
                    self.bar_url.clearFocus()
                else:
                    url = "https://duckduckgo.com/?q=" + url
                    self.bar_url.setText(url)
                    self.browser.setUrl(QUrl(url))
                    self.bar_url.clearFocus()
                    return
            else:
                self.browser.setUrl(QUrl(url))
                self.bar_url.clearFocus()

    def updateURLBar(self, url):
        self.bar_url.setText(url.toString())

    def updateWindowTitle(self, title):
        self.setWindowTitle(f"{title} - JotaWeb")

class CustomToolBar(QToolBar):
    def __init__(self):
        super().__init__()

    def allowedAreas(self):
        return Qt.TopToolBarArea | Qt.BottomToolBarArea | Qt.ToolBarArea

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