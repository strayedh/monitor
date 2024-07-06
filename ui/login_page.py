from PyQt5 import QtWidgets, QtGui, QtCore
from services.user_manager import UserManager

class LoginPage(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.user_manager = UserManager()

    def initUI(self):
        self.setWindowTitle('登录')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout()

        self.backgroundLabel = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("resources/tech_background.jpg")
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setGeometry(0, 0, 400, 300)
        self.backgroundLabel.setScaledContents(True)
        self.layout.addWidget(self.backgroundLabel)

        self.formLayout = QtWidgets.QFormLayout()

        self.usernameLabel = QtWidgets.QLabel('用户名:', self)
        self.usernameLabel.setStyleSheet("color: white; font-size: 16px;")
        self.formLayout.addRow(self.usernameLabel, self.createInputField())

        self.passwordLabel = QtWidgets.QLabel('密码:', self)
        self.passwordLabel.setStyleSheet("color: white; font-size: 16px;")
        self.formLayout.addRow(self.passwordLabel, self.createPasswordField())

        self.loginButton = QtWidgets.QPushButton('登录', self)
        self.loginButton.setStyleSheet("background: white; color: black; font-size: 16px;")
        self.loginButton.clicked.connect(self.login)
        self.formLayout.addRow(self.loginButton)

        self.layout.addLayout(self.formLayout)
        self.setLayout(self.layout)
        self.setStyleSheet("background: transparent;")
        self.backgroundLabel.lower()

    def createInputField(self):
        inputField = QtWidgets.QLineEdit(self)
        inputField.setStyleSheet("background: white; color: black; font-size: 16px;")
        return inputField

    def createPasswordField(self):
        passwordField = QtWidgets.QLineEdit(self)
        passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        passwordField.setStyleSheet("background: white; color: black; font-size: 16px;")
        return passwordField

    def login(self):
        username = self.formLayout.itemAt(1).widget().text()
        password = self.formLayout.itemAt(3).widget().text()
        if self.user_manager.login(username, password):
            self.show_message('成功', '登录成功')
            self.main_window.showVideoRecognitionApp()
            self.close()
        else:
            self.show_message('错误', '用户名或密码错误')

    def show_message(self, title, message):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStyleSheet("QLabel { color: black; } QWidget { background: white; }")
        msgBox.exec_()
