import sys
from PyQt5 import QtWidgets
from ui.login_page import LoginPage
from ui.register_page import RegisterPage
from ui.video_recognition_app import VideoRecognitionApp

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('视频识别系统')
        self.setGeometry(100, 100, 300, 200)

        self.layout = QtWidgets.QVBoxLayout()

        self.loginButton = QtWidgets.QPushButton('登录', self)
        self.loginButton.clicked.connect(self.showLoginPage)
        self.layout.addWidget(self.loginButton)

        self.registerButton = QtWidgets.QPushButton('注册', self)
        self.registerButton.clicked.connect(self.showRegisterPage)
        self.layout.addWidget(self.registerButton)

        self.setLayout(self.layout)

    def showLoginPage(self):
        self.loginPage = LoginPage(self)
        self.loginPage.show()
        self.hide()

    def showRegisterPage(self):
        self.registerPage = RegisterPage(self)
        self.registerPage.show()
        self.hide()

    def showVideoRecognitionApp(self):
        self.videoRecognitionApp = VideoRecognitionApp()
        self.videoRecognitionApp.show()
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
