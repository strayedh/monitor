from PyQt5 import QtWidgets, QtGui, QtCore
from ui.video_recognition_app import VideoRecognitionApp

class StartPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('视频识别系统')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QtWidgets.QVBoxLayout()

        self.backgroundLabel = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("resources/tech_background.jpg")
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.backgroundLabel)

        self.enterButton = QtWidgets.QPushButton('进入系统', self)
        self.enterButton.clicked.connect(self.enterSystem)
        self.enterButton.setStyleSheet("font-size: 18px; padding: 10px 20px;")
        self.layout.addWidget(self.enterButton, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

    def enterSystem(self):
        self.hide()
        self.video_recognition_app = VideoRecognitionApp()
        self.video_recognition_app.show()
