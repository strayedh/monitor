from PyQt5 import QtWidgets, QtGui
from services.baidu_api import BaiduAPI
from services.video_processing import VideoProcessing
from utils.image_utils import annotate_image
from utils.file_utils import save_detected_frame
import threading
import cv2


class VideoRecognitionApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.api = BaiduAPI()
        self.video_processing = VideoProcessing(self.update_frame)
        self.detected_frames = []
        self.current_index = -1

    def initUI(self):
        self.setWindowTitle('视频识别应用')
        self.setGeometry(100, 100, 1000, 600)  # Adjusted width and height

        self.main_layout = QtWidgets.QHBoxLayout()

        # Left layout for images and controls
        self.left_layout = QtWidgets.QVBoxLayout()

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setFixedSize(600, 400)
        self.left_layout.addWidget(self.imageLabel)

        self.loadButton = QtWidgets.QPushButton('加载视频', self)
        self.loadButton.clicked.connect(self.loadVideo)
        self.left_layout.addWidget(self.loadButton)

        self.detectButton = QtWidgets.QPushButton('检测当前帧', self)
        self.detectButton.clicked.connect(self.detectCurrentFrame)
        self.left_layout.addWidget(self.detectButton)

        self.saveButton = QtWidgets.QPushButton('保存当前检测到的图像', self)
        self.saveButton.clicked.connect(self.saveCurrentFrame)
        self.left_layout.addWidget(self.saveButton)

        self.prevButton = QtWidgets.QPushButton('上一张', self)
        self.prevButton.clicked.connect(self.showPreviousFrame)
        self.left_layout.addWidget(self.prevButton)

        self.nextButton = QtWidgets.QPushButton('下一张', self)
        self.nextButton.clicked.connect(self.showNextFrame)
        self.left_layout.addWidget(self.nextButton)

        self.resultImageLabel = QtWidgets.QLabel(self)
        self.resultImageLabel.setFixedSize(600, 400)
        self.left_layout.addWidget(self.resultImageLabel)

        self.main_layout.addLayout(self.left_layout)

        # Right layout for result text
        self.right_layout = QtWidgets.QVBoxLayout()

        self.resultLabel = QtWidgets.QLabel(self)
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setFixedSize(350, 400)  # Adjusted size to fit the main window
        self.right_layout.addWidget(self.resultLabel)

        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

    def loadVideo(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "加载视频", "",
                                                            "视频文件 (*.mp4 *.avi *.mov);;所有文件 (*)",
                                                            options=options)
        if fileName:
            print(f"Loading video: {fileName}")
            self.video_processing.load_video(fileName)

    def detectCurrentFrame(self):
        if self.video_processing.current_frame is not None:
            threading.Thread(target=self.process_frame, args=(self.video_processing.current_frame,),
                             daemon=True).start()

    def process_frame(self, frame):
        combined_result = self.api.detect(frame)
        self.display_results(frame, combined_result)
        self.detected_frames.append((frame, combined_result))
        self.current_index = len(self.detected_frames) - 1

    def saveCurrentFrame(self):
        if self.current_index != -1:
            frame, result = self.detected_frames[self.current_index]
            save_detected_frame(frame, result, self.resultLabel.text())

    def display_results(self, frame, result):
        self.resultLabel.setText(f"检测到的人数：{result['person_num']}\n检测到的车辆：\n" + "\n".join(
            [f"{k}：{v}" for k, v in result['vehicle_num'].items()]))
        width, height = self.resultImageLabel.size().width(), self.resultImageLabel.size().height()
        annotated_image = annotate_image(frame, result, self.resultLabel.text(), width, height)
        self.resultImageLabel.setPixmap(QtGui.QPixmap.fromImage(annotated_image))

    def update_frame(self, frame):
        width, height = self.imageLabel.size().width(), self.imageLabel.size().height()
        frame_resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        rgb_image = QtGui.QImage(frame_resized.data, frame_resized.shape[1], frame_resized.shape[0],
                                 frame_resized.strides[0], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(rgb_image))

    def showPreviousFrame(self):
        if self.current_index > 0:
            self.current_index -= 1
            frame, result = self.detected_frames[self.current_index]
            self.display_results(frame, result)

    def showNextFrame(self):
        if self.current_index < len(self.detected_frames) - 1:
            self.current_index += 1
            frame, result = self.detected_frames[self.current_index]
            self.display_results(frame, result)
