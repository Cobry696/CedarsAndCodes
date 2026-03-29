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
    QSizePolicy,
    QListWidget,
    QCompleter,
    QListWidgetItem,
    QListView
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

        self.setCentralWidget(loginPage)

    def loggedIn(self, isLoggedIn, val1, val2): # named val as we do not know which is username and which is email
        if isLoggedIn:
            print("Congrats")
            self.homePage = HomePage()
            if re.match(r".+@.+\..+", val1):
                #print(val2,val1)
                self.homePage.username = val2
                self.homePage.email = val1
            else:
                #print(val1,val2)
                self.homePage.username = val1
                self.homePage.email = val2
            self.setCentralWidget(self.homePage)

class LoginPage(QWidget):
    # signal for teeling the program to log in
    logInSignal = Signal(bool, str, str)
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
        self.pwordEntry.returnPressed.connect(self.logInButtonClicked)

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
        username, password = self.unameEntry.text(), self.pwordEntry.text()
        loginResult = cnc.Login(username, password, True) # contains the loggedin boolean and the missing piece the user did not enter
        if isinstance(loginResult, tuple):
            isLoggedIn = loginResult[0]
            missing = loginResult[1] # this part helps us get the email/username that the user doesnt enter so we can use it when they upload code
            self.logInSignal.emit(isLoggedIn, username, missing) # telling the program we have attempted a login
        else: # if login result is just a bool
            isLoggedIn = loginResult
            self.logInSignal.emit(isLoggedIn, username, "") # telling the program we have attempted a login. send an empty string for the missing as its false so it doesnt matter
        
    def newButtonClicked(self):
        self.unameEntry.setPlaceholderText("Username")
        self.emailEntry.show()
        self.nameLayoutWidget.show()
        self.titleLabel.setText("Create Account")
        self.upperButton.setCurrentIndex(1)
        self.lowerButton.setCurrentIndex(1)
    def createAccountButtonClicked(self):
        username, email = self.unameEntry.text(), self.emailEntry.text()
        isLoggedIn = cnc.CreateUser(username, email, self.pwordEntry.text(), self.fnameEntry.text(), self.lnameEntry.text())
        self.logInSignal.emit(isLoggedIn, username, email) # telling the program we have attempted a login
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
        self.username = "" # will be set by the main window when created
        self.email = "" # will be set by the main window when created

        self.grid = QGridLayout()
        self.searchBy = "Title"
        self.addPanelOpen = False

        # labels
        self.titleLabel = QLabel("Cedars & Codes")
        
        # entries
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search")
        self.searchEntry.returnPressed.connect(self.search)

        # adding entries
        self.addTitleEntry = QLineEdit()
        self.addTitleEntry.setPlaceholderText("Title")
        self.addTitleEntry.hide()

        self.addDescriptionEntry = QTextEdit()
        self.addDescriptionEntry.setPlaceholderText("Description")
        self.addDescriptionEntry.hide()

        self.addCodeEntry = QTextEdit()
        self.addCodeEntry.setPlaceholderText("Code")
        self.addCodeEntry.hide()

        # BUTTONS!!!!
        self.addButton = SquareButton("+")
        self.addButton.setStyleSheet("font-size: 60pt; font-weight: bold")
        self.addButton.clicked.connect(self.toggleAddPanel)

        self.submitSnippetButton = QPushButton("Submit")
        self.submitSnippetButton.clicked.connect(self.submitCodeSnippet)
        self.submitSnippetButton.hide()

        self.logoutButton = QPushButton("Logout")
        self.logoutButton.clicked.connect(self.logoutButtonClicked)

        # drop downs
        self.languages = [i[0] for i in cnc.get_languages()]
        self.languageDropdown = QComboBox()
        self.languageDropdown.setPlaceholderText("Language")
        self.languageDropdown.currentTextChanged.connect(self.changeLanguage)
        self.languageDropdown.addItems(self.languages)
        
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
                "None"
            ]
            

        self.outputDropdown = SearchableDropdown()
        self.outputDropdown.lineEdit().setPlaceholderText("Output Type")
        self.outputDropdown.currentTextChanged.connect(self.changeOutput)
        self.outputDropdown.addItems(types)
        self.outputDropdown.setCurrentIndex(-1) # makes sure it starts on placeholder text

        self.inputDropdown = SearchableDropdown()
        self.inputDropdown.lineEdit().setPlaceholderText("Input Types")
        self.inputDropdown.currentTextChanged.connect(self.changeInput)
        self.inputDropdown.addItems(types)
        self.inputDropdown.setCurrentIndex(-1) # makes sure it starts on placeholder text

        # dropdowns for adding
        self.addLanguageDropdown = QComboBox()
        self.addLanguageDropdown.setPlaceholderText("Language")
        self.addLanguageDropdown.currentTextChanged.connect(self.changeLanguage)
        self.addLanguageDropdown.addItems(self.languages)
        self.addLanguageDropdown.hide()
        
        self.addOutputDropdown = SearchableDropdown()
        self.addOutputDropdown.lineEdit().setPlaceholderText("Output Type")
        self.addOutputDropdown.currentTextChanged.connect(self.changeOutput)
        self.addOutputDropdown.addItems(types)
        self.addOutputDropdown.setCurrentIndex(-1) # makes sure it starts on placeholder text
        self.addOutputDropdown.hide()
        self.addOutputDropdown.list.hide()

        self.addInputDropdown = SearchableDropdown()
        self.addInputDropdown.lineEdit().setPlaceholderText("Input Types")
        self.addInputDropdown.currentTextChanged.connect(self.changeInput)
        self.addInputDropdown.addItems(types)
        self.addInputDropdown.setCurrentIndex(-1) # makes sure it starts on placeholder text
        self.addInputDropdown.hide()
        self.addInputDropdown.list.hide()

        # snippet list
        self.snippetList = SnippetList()

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
        self.grid.addWidget(self.logoutButton, 1,0)

        self.grid.addWidget(self.titleLabel, 0,0)
        self.grid.addWidget(self.searchEntry, 1,3, 1, 3)
        self.grid.addWidget(self.languageDropdown, 1,6)
        self.grid.addWidget(self.inputDropdown, 0,5)
        self.grid.addWidget(self.outputDropdown, 0,6)
        self.grid.addWidget(self.searchByDropdown, 0, 3)
        self.grid.addWidget(self.addButton, 6, 0)

        self.grid.addWidget(self.inputDropdown.list, 2,5)
        self.grid.addWidget(self.outputDropdown.list, 2,6)

        # for adding the add stuff to the grid
        self.grid.addWidget(self.addTitleEntry, 3,3)
        self.grid.addWidget(self.addDescriptionEntry, 4,3)
        self.grid.addWidget(self.addCodeEntry, 5,3)
        self.grid.addWidget(self.submitSnippetButton, 5,4)
        self.grid.addWidget(self.addLanguageDropdown, 4,5)
        self.grid.addWidget(self.addInputDropdown, 5,5)
        self.grid.addWidget(self.addOutputDropdown, 5,6)

        self.grid.addWidget(self.addInputDropdown.list, 6,5)
        self.grid.addWidget(self.addOutputDropdown.list, 6,6)

        # snippetList
        self.grid.addWidget(self.snippetList, 2,2,3,3)
        
        # self.grid.addWidget()
        # self.grid.addWidget()

        self.setLayout(self.grid)

    def changeLanguage(self, text):
        pass

    def changeOutput(self, text):
        pass

    def changeInput(self, text):
        pass

    def search(self): # connect with database and add the matching snippets to a list
        snippets = cnc.fetch_snippets(self.searchEntry.text(), self.searchBy, self.languageDropdown.currentText(), self.inputDropdown.listItems, self.outputDropdown.listItems)
        #print(snippets)
        self.snippetList.clear()
        self.snippetList.addSnippets(snippets)

    def searchByChanged(self, text):
        if text != "Title":
            self.searchBy = "Description"
        else:
            self.searchBy = "Title"

    def toggleAddPanel(self):
        if self.addPanelOpen:
            self.addButton.setText("+")
            self.addTitleEntry.hide()
            self.addDescriptionEntry.hide()
            self.addCodeEntry.hide()
            self.submitSnippetButton.hide()
            self.addLanguageDropdown.hide()
            self.addOutputDropdown.hide()
            self.addOutputDropdown.list.hide()
            self.addInputDropdown.hide()
            self.addInputDropdown.list.hide()

            self.snippetList.show() # toggles on when the panel is hidden
        else:
            self.addButton.setText("-")
            self.addTitleEntry.show()
            self.addDescriptionEntry.show()
            self.addCodeEntry.show()
            self.submitSnippetButton.show()
            self.addLanguageDropdown.show()
            self.addOutputDropdown.show()
            self.addOutputDropdown.list.show()
            self.addInputDropdown.show()
            self.addInputDropdown.list.show()

            self.snippetList.hide() # toggles off when the panel is brought up

        self.addPanelOpen = not self.addPanelOpen # toggle the panel

    def submitCodeSnippet(self):
        cnc.AddSnippet(self.email, self.addTitleEntry.text(), self.addCodeEntry.toPlainText(), self.addDescriptionEntry.toPlainText(), ",".join(self.addInputDropdown.listItems), ",".join(self.addOutputDropdown.listItems), self.addLanguageDropdown.currentText())
        self.toggleAddPanel()

    def logoutButtonClicked(self):
        QApplication.instance().quit()

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

class SearchableDropdown(QComboBox): # this is mainly for the type dropdowns
    def __init__(self):
        super().__init__()

        # these are the lines that make it searchable
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.activated.connect(self.addItemToList)

        # this will make it multiselect
        self.listItems = []
        self.list = QListWidget() # a display underneath the dropdown that will contain the currently selected types

    def addItemToList(self): # multiselect stuff
        t = self.currentText()
        # weird bug where if you add and remove an item the panel takes two button presses to reopen
        def clear_self():
            print(t)
            self.listItems.remove(t)
            takenItem = self.list.takeItem(self.list.row(item))
            if takenItem:
                del takenItem
            
            
        if t not in self.listItems:
            # adds an item to the list
            self.listItems.append(self.currentText())
            item = QListWidgetItem()
            button = QPushButton(self.currentText())
            button.clicked.connect(clear_self)
            self.list.addItem(item)
            self.list.setItemWidget(item, button)
            self.sizeHint=button.sizeHint

        self.setCurrentIndex(-1) # sets back to placeholder text

class SnippetList(QListWidget):
    def __init__(self):
        super().__init__()
    
    def addSnippets(self, snippets):
        for snippet in snippets:
            item = QListWidgetItem()
            snippetButton = Snippet(snippet[1], snippet[2], snippet[3])
            item.setSizeHint(snippetButton.size())
            self.addItem(item)
            self.setItemWidget(item, snippetButton)
        
class Snippet(QPushButton):
    def __init__(self, title, body, description):
        super().__init__()
        self.clicked.connect(self.openCopyDialog)
        self.title = title
        self.description = description
        self.body = body

        self.setText(title)
        self.setStyleSheet("font-size: 20pt; font-weight: bold")
        self.setToolTip(description)

        # layout = QHBoxLayout(self) # allowing us to add two bits of text to the button
        # self.setLayout(layout)

        # self.title = QLabel(title)
        # self.title.setStyleSheet("font-size: 20pt")

        # self.description = QLabel(description)
        # self.description.setStyleSheet("font-size: 10pt")

        # layout.addWidget(self.title)
        # layout.addWidget(self.description)

    def openCopyDialog(self):
        copyDialog = QMessageBox()
        copyDialog.setWindowTitle(self.title)
        copyDialog.setText(self.body)
        copyDialog.setIcon(QMessageBox.Icon.Information)
        copyButton = copyDialog.addButton("Copy", QMessageBox.ButtonRole.ActionRole)
        copyDialog.exec()
        if copyDialog.clickedButton() == copyButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.body)



        

        

window = MainWindow()
window.show()

app.exec()