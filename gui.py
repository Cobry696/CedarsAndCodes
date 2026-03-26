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
import qdarktheme

app = QApplication(sys.argv)
app.setStyle("Fusion")
stylesheet = qdarktheme.load_stylesheet()
app.setStyleSheet(stylesheet)

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
        unameEntry.setPlaceholderText("Username")

        pwordEntry = QLineEdit()
        pwordEntry.setEchoMode(QLineEdit.Password) # makes the password display as dots
        pwordEntry.setPlaceholderText("Password")

        # labels for page title and username/password entries
        titleLabel = QLabel("Login/Sign Up")

        # actually adding the widgets to the layout
        layout.addWidget(titleLabel)
        layout.addWidget(unameEntry)
        layout.addWidget(pwordEntry)
        

        

window = MainWindow()
window.show()

app.exec()