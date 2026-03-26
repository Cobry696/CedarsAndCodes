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

        self.layout1 = QVBoxLayout()
        self.layout1.setContentsMargins(200,200,200,600)
        self.setLayout(self.layout1)

        # text inputs for username and password
        unameEntry = QLineEdit()
        unameEntry.setPlaceholderText("Username/Email")

        pwordEntry = QLineEdit()
        pwordEntry.setEchoMode(QLineEdit.Password) # makes the password display as dots
        pwordEntry.setPlaceholderText("Password")

        # entry for email
        emailEntry = QLineEdit()
        emailEntry.setPlaceholderText("Email")

        # labels for page title and username/password entries
        titleLabel = QLabel("Login/Sign Up")

        # BUTTONS!!!
        loginButton = QPushButton("Login")
        signupButton = QPushButton("Sign Up")

        # actually adding the widgets to the layout
        self.layout1.addWidget(titleLabel)
        self.layout1.addWidget(unameEntry)
        self.layout1.addWidget(pwordEntry)
        self.layout1.addWidget(loginButton)
        self.layout1.addWidget(signupButton)

    # button events
    def logInButton(self):
        pass
    def signUpButton(self):
        self.layout1.addWidget()

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        self.layout1.setContentsMargins(height*0.2, width*0.2, height*0.2, width*0.2)
        

        

window = MainWindow()
window.show()

app.exec()