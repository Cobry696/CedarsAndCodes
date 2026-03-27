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
    QStackedWidget,
    QSizePolicy
)

# Hi
from PySide6.QtCore import QSize, Qt, QObject, Signal
from PySide6.QtGui import QAction, QIcon, QKeySequence, QFontDatabase, QFont, QTextCursor, QShortcut, QTextDocument
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys
import re
import qdarktheme
import cedarsandcodes as cnc

app = QApplication(sys.argv)
app.setStyle("Fusion")
stylesheet = qdarktheme.load_stylesheet()
app.setStyleSheet(stylesheet) # dark mode baby

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cedars&Codes")

        loginPage = LoginPage()
        loginPage.logInSignal.connect(self.loggedIn)

        self.homePage = HomePage()

        self.setCentralWidget(loginPage)

    def loggedIn(self, isLoggedIn):
        if isLoggedIn:
            print("Congrats")
            self.setCentralWidget(self.homePage)

class LoginPage(QWidget):
    # signal for teeling the program to log in
    logInSignal = Signal(bool)
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
        self.loginButton.clicked.connect(self.logInButtonClicked)

        self.signupButton = QPushButton("New? Go To Account Creation")
        self.signupButton.clicked.connect(self.newButtonClicked)

        self.createAccountButton = QPushButton("Create Account")
        self.createAccountButton.clicked.connect(self.createAccountButtonClicked)

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
        isLoggedIn = cnc.Login(self.unameEntry.text(), self.pwordEntry.text()) # have to add fname and lname # uncomment
        self.logInSignal.emit(isLoggedIn) # telling the program we have attempted a login. replace with isLoggedIn instead of true
    def newButtonClicked(self):
        self.unameEntry.setPlaceholderText("Username")
        self.emailEntry.show()
        self.nameLayoutWidget.show()
        self.titleLabel.setText("Create Account")
        self.upperButton.setCurrentIndex(1)
        self.lowerButton.setCurrentIndex(1)
    def createAccountButtonClicked(self):
        isLoggedIn = cnc.CreateUser(self.unameEntry.text(), self.emailEntry.text(), self.pwordEntry.text(), self.fnameEntry.text(), self.lnameEntry.text())
        self.logInSignal.emit(isLoggedIn) # telling the program we have attempted a login
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

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.searchBy = "Title"

        # labels
        self.titleLabel = QLabel("Cedars & Codes")
        
        # entries
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search")
        self.searchEntry.returnPressed.connect(self.search)

        # BUTTONS!!!!
        self.addButton = SquareButton("+")

        # drop downs
        self.languageDropdown = QComboBox()
        self.languageDropdown.setPlaceholderText("Language")
        self.languageDropdown.currentTextChanged.connect(self.changeLanguage)
        self.languageDropdown.addItems( # should change to be based on what rows are in the table
            [
                "Python",
                "C",
                "Java",
                "Rust",
                "C++"
            ]
        )
        
        self.searchByDropdown = QComboBox()
        self.searchByDropdown.setPlaceholderText("Search By...")
        self.searchByDropdown.currentTextChanged.connect(self.searchByChanged)
        self.searchByDropdown.addItems([
            "Title",
            "Description"
        ])

        types = [ # change to pull from the table data
                "Int",
                "Float",
                "String",
                "Object",
                "Other",
                "Array-Int",
                "Array-Float",
                "Array-String",
                "Array-Object",
                "Array-Other",
            ]
            

        self.outputDropdown = QComboBox()
        self.outputDropdown.setPlaceholderText("Output Type")
        self.outputDropdown.currentTextChanged.connect(self.changeOutput)
        self.outputDropdown.addItems(types)

        # gonna wanna use QCompleter instead so we can select multiple input types
        self.inputDropdown = QComboBox()
        self.inputDropdown.setPlaceholderText("Input Type")
        self.inputDropdown.currentTextChanged.connect(self.changeInput)
        self.inputDropdown.addItems(types)

        # changing grid stretching
        self.grid.setColumnStretch(0,1)
        self.grid.setColumnStretch(1,1)
        self.grid.setColumnStretch(2,1)
        self.grid.setColumnStretch(3,1)
        self.grid.setColumnStretch(4,1)
        self.grid.setColumnStretch(5,1)
        self.grid.setColumnStretch(6,1)

        self.grid.setRowStretch(0,1)
        self.grid.setRowStretch(1,1)
        self.grid.setRowStretch(2,1)
        self.grid.setRowStretch(3,1)
        self.grid.setRowStretch(4,1)
        self.grid.setRowStretch(5,1)
        self.grid.setRowStretch(6,1)

        # add to layout and display
        self.grid.addWidget(self.titleLabel, 0,0)
        self.grid.addWidget(self.searchEntry, 1,3, 1, 3)
        self.grid.addWidget(self.languageDropdown, 1,6)
        self.grid.addWidget(self.inputDropdown, 0,5)
        self.grid.addWidget(self.outputDropdown, 0,6)
        self.grid.addWidget(self.searchByDropdown, 0, 3)
        self.grid.addWidget(self.addButton, 6, 0)

        self.setLayout(self.grid)

    def changeLanguage(self, text): # gets the text of the new language selected and uses it to alter the types shown in the output dropdown and input selector
        pass

    def changeOutput(self, text):
        pass

    def changeInput(self, text):
        pass

    def search(self, term): # connect with database
        pass

    def searchByChanged(self, text):
        if text != "Title":
            self.searchBy = "Description"
        else:
            self.searchBy = "Title"

class SquareButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # Allow vertical and horizontal expanding
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def hasHeightForWidth(self):
        # Indicate that the height depends on the width
        return True

    def heightForWidth(self, width):
        # Force height to be equal to width
        return width


        

        

window = MainWindow()
window.show()

app.exec()