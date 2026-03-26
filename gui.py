from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton,
    QStatusBar,
    QToolBar,
    QWidget,
    QTabWidget,
    QGridLayout,
    QLabel,
    QMessageBox,
    QComboBox,
    QTextEdit,
    QScrollArea,
    QVBoxLayout,
    QLineEdit
)

# Hi
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QFontDatabase, QFont, QTextCursor, QShortcut, QTextDocument
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys
import re

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cedars&Codes")

        self.setCentralWidget(LoginPage())

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(200,200,200,600)
        self.setLayout(layout)

        # text inputs for username and password
        unameEntry = QLineEdit()
        pwordEntry = QLineEdit()
        pwordEntry.setEchoMode(QLineEdit.Password) # makes the password display as dots

        # labels for page title and username/password entries
        titleLabel = QLabel("Login/Sign Up")
        unameLabel = QLabel("Username:")
        pwordLabel = QLabel("Password:")

        # actually adding the widgets to the layout
        layout.addWidget(titleLabel)
        layout.addWidget(unameLabel)
        layout.addWidget(unameEntry)
        layout.addWidget(pwordLabel)
        layout.addWidget(pwordEntry)

        

        

window = MainWindow()
window.show()

app.exec()