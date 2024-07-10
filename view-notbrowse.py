# Import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QWidget

START_URL = "http://google.com" # Example URL

# Main class
class JotaleaWebView(QMainWindow):
    # The function that runs when running the class
    def __init__(self, *args, **kwargs):
        super(JotaleaWebView, self).__init__(*args, **kwargs)

        # Create a Qt window and name it
        self.window = QWidget()
        self.window.setWindowTitle("Jotalea WebView")

        # Create a Qt layout
        self.layout = QVBoxLayout()

        # Create a webview instance
        self.browser = QWebEngineView()

        # Add the webview to the layout
        self.layout.addWidget(self.browser)

        # Set the webview's URL to the assigned URL
        self.browser.setUrl(QUrl(START_URL))

        # Apply the layout to the window
        self.window.setLayout(self.layout)

        # Show the window to the user
        self.window.show()

# Initialize the Qt Application
app = QApplication([])

# Invoke the main window
window = JotaleaWebView()

# Run
app.exec_()
