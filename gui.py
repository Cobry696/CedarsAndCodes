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
    QLineEdit,
    QHBoxLayout,
    QStackedWidget
)

# Hi
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QFontDatabase, QFont, QTextCursor, QShortcut, QTextDocument
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys
import re
import qdarktheme
#import cedarsandcodes as cnc

app = QApplication(sys.argv)
app.setStyle("Fusion")
stylesheet = qdarktheme.load_stylesheet()
app.setStyleSheet(stylesheet) # dark mode baby

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
        self.unameEntry = QLineEdit()
        self.unameLayout = QHBoxLayout() # this layout will hold the username entry as well as the email entry if the user is creating an account
        self.unameEntry.setPlaceholderText("Username/Email")

        self.pwordEntry = QLineEdit()
        self.pwordEntry.setEchoMode(QLineEdit.Password) # makes the password display as dots
        self.pwordEntry.setPlaceholderText("Password")

        # entry for email
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Email")
        self.emailEntry.hide()
        
        # first and last names
        self.nameLayout = QHBoxLayout()

        self.fnameEntry = QLineEdit()
        self.fnameEntry.setPlaceholderText("First Name")
        self.nameLayout.addWidget(self.fnameEntry)

        self.lnameEntry = QLineEdit()
        self.lnameEntry.setPlaceholderText("Last Name")
        self.nameLayout.addWidget(self.lnameEntry)
        self.nameLayout.setContentsMargins(0,0,0,0)

        self.nameLayoutWidget = QWidget()
        self.nameLayoutWidget.setLayout(self.nameLayout)
        self.nameLayoutWidget.hide() # hides the name entry when logging in
        

        # labels for page title and username/password entries
        self.titleLabel = QLabel("Log In")

        # BUTTONS!!!
        self.loginButton = QPushButton("Login")
        self.signupButton = QPushButton("New? Go To Account Creation")
        self.signupButton.clicked.connect(self.newButtonClicked)

        self.createAccountButton = QPushButton("Create Account")
        self.goBackToLoginButton = QPushButton("Go back to login")
        self.goBackToLoginButton.clicked.connect(self.backToLoginButtonClicked)

        # stacked widgets for changing stuff
        # upper button contains either the login button or the create account button. It is alwasy the button to confirm the action
        self.upperButton = QStackedWidget()
        self.upperButton.addWidget(self.loginButton)
        self.upperButton.addWidget(self.createAccountButton)
        # lower button contains the button to alter the screen to either create account or login
        self.lowerButton = QStackedWidget()
        self.lowerButton.addWidget(self.signupButton)
        self.lowerButton.addWidget(self.goBackToLoginButton)

        # adding widgets to sub layouts
        self.unameLayout.addWidget(self.unameEntry)
        self.unameLayout.addWidget(self.emailEntry)
        self.unameLayout.setContentsMargins(0,0,0,0) # fixes the little gap at the side of the boxes
        # setting the layout to a dummy widget
        unameLayoutWidget = QWidget()
        unameLayoutWidget.setLayout(self.unameLayout)

        # actually adding the widgets to the layout
        self.layout1.addWidget(self.titleLabel)
        self.layout1.addWidget(self.nameLayoutWidget)
        self.layout1.addWidget(unameLayoutWidget)
        self.layout1.addWidget(self.pwordEntry)
        self.layout1.addWidget(self.upperButton)
        self.layout1.addWidget(self.lowerButton)

    # button events
    def logInButtonClicked(self):
        cnc.Login(self.unameEntry.text(), self.pwordEntry.text()) # have to add fname and lname
    def newButtonClicked(self):
        self.unameEntry.setPlaceholderText("Username")
        self.emailEntry.show()
        self.nameLayoutWidget.show()
        self.titleLabel.setText("Create Account")
        self.upperButton.setCurrentIndex(1)
        self.lowerButton.setCurrentIndex(1)
    def createAccountButtonClicked(self):
        cnc.CreateUser(self.unameEntry.text(), self.emailEntry.text(), self.pwordEntry.text(), self.fnameEntry.text(), self.lnameEntry.text())
    def backToLoginButtonClicked(self):
        self.unameEntry.setPlaceholderText("Username/Email")
        self.emailEntry.hide()
        self.nameLayoutWidget.hide()
        self.titleLabel.setText("Log In")
        self.upperButton.setCurrentIndex(0)
        self.lowerButton.setCurrentIndex(0)

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        self.layout1.setContentsMargins(width*0.2, height*0.2, width*0.2, height*0.2)
        

        

window = MainWindow()
window.show()

app.exec()