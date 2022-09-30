import cv2
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QGridLayout,
    QApplication,
)

from RobotToolWidgets import JogPanel, MoxaVisual, PoseWidget, TeachPanel, Slider


class Worker(QObject):
    change_pixmap = pyqtSignal(QImage)

    # @pyqtSlot(int, int)
    # def set_widget_size(self, width: int, height: int):
    #     print("set_widget_size", width, height)
    #     self.width = width
    #     self.height = height

    def run(self):
        width, height = 400, 300
        x, y = int(width / 2), int(height / 2)

        capture = cv2.VideoCapture(0)
        # get the width and height of the frame
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        while not QThread.currentThread().isInterruptionRequested():
            ret, cv_img = capture.read()
            if not ret:
                continue

            for radius in range(25, 201, 25):
                cv2.circle(cv_img, (x, y), radius, (0, 0, 255), 1)

            # Vertical line
            cv2.line(cv_img, (x, 0), (x, height), (0, 0, 255), 1)
            # Horizontal line
            cv2.line(cv_img, (0, y), (width, y), (0, 0, 255), 1)

            rgbImage = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.change_pixmap.emit(p)


class CameraDisplay(QLabel):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.setText("Loading OpenCV...")
        self.setFixedSize(400, 300)

    # def resizeEvent(self, event):
    #     self.width = event.size().width()
    #     self.height = event.size().height()
    #     self.window.signal_send_size_to_worker.emit(self.width, self.height)


class MainWindow(QMainWindow):
    signal_send_size_to_worker = pyqtSignal(int, int)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Mecademic Robot")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.left_layout = QVBoxLayout()
        self.central_layout.addLayout(self.left_layout)

        self.jog_widget = JogPanel()
        self.left_layout.addWidget(self.jog_widget)

        self.teach_panel = TeachPanel(self)
        self.slider_1 = Slider()
        self.slider_1.valueChanged.connect(lambda: self.teach_panel.set_orientation(1, self.slider_1.value()))
        self.left_layout.addWidget(self.slider_1)

        self.slider_2 = Slider()
        self.slider_2.valueChanged.connect(lambda: self.teach_panel.set_orientation(2, self.slider_2.value()))
        self.left_layout.addWidget(self.slider_2)

        self.slider_3 = Slider()
        self.slider_3.valueChanged.connect(lambda: self.teach_panel.set_orientation(3, self.slider_3.value()))
        self.left_layout.addWidget(self.slider_3)

        self.slider_4 = Slider()
        self.slider_4.valueChanged.connect(lambda: self.teach_panel.set_orientation(4, self.slider_4.value()))
        self.left_layout.addWidget(self.slider_4)

        self.slider_5 = Slider()
        self.slider_5.valueChanged.connect(lambda: self.teach_panel.set_orientation(5, self.slider_5.value()))
        self.left_layout.addWidget(self.slider_5)

        self.slider_6 = Slider()
        self.slider_6.valueChanged.connect(lambda: self.teach_panel.set_orientation(6, self.slider_6.value()))
        self.left_layout.addWidget(self.slider_6)

        self.mid_layout = QVBoxLayout()
        self.central_layout.addLayout(self.mid_layout)

        self.joint_pose = PoseWidget([f"J{i}" for i in range(1, 7)])
        self.mid_layout.addWidget(self.joint_pose)

        self.tcp_pose = PoseWidget(["X", "Y", "Z", "Alpha", "Beta", "Gamma"])
        self.mid_layout.addWidget(self.tcp_pose)

        self.mid_layout.addWidget(self.teach_panel)

        self.right_layout = QVBoxLayout()
        self.central_layout.addLayout(self.right_layout)

        self.error_label = QLabel("No Error")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.error_label)

        self.actions_layout = QGridLayout()
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.addLayout(self.actions_layout)

        self.push_button_connect = QPushButton("Connect")
        self.actions_layout.addWidget(self.push_button_connect, 0, 0)

        self.push_button_disconnect = QPushButton("Disconnect")
        self.actions_layout.addWidget(self.push_button_disconnect, 0, 1)

        self.push_button_activate = QPushButton("Activate")
        self.actions_layout.addWidget(self.push_button_activate, 1, 0)

        self.push_button_home = QPushButton("Home")
        self.actions_layout.addWidget(self.push_button_home, 1, 1)

        self.push_button_unpause = QPushButton("Unpause")
        self.actions_layout.addWidget(self.push_button_unpause, 2, 0)

        self.push_button_stop = QPushButton("Stop")
        self.actions_layout.addWidget(self.push_button_stop, 2, 1)

        self.push_button_reset = QPushButton("Reset")
        self.actions_layout.addWidget(self.push_button_reset, 3, 0)

        self.push_button_start = QPushButton("Start")
        self.actions_layout.addWidget(self.push_button_start, 3, 1)

        self.push_button_test = QPushButton("test")
        self.actions_layout.addWidget(self.push_button_test, 4, 0)

        self.push_button_generate = QPushButton("Generate Script")
        self.actions_layout.addWidget(self.push_button_generate, 4, 1)

        self.use_moxa = QCheckBox("Use Moxa")
        self.right_layout.addWidget(self.use_moxa, 0, Qt.AlignCenter)

        self.moxa_ip_layout = QHBoxLayout()
        self.right_layout.addLayout(self.moxa_ip_layout)

        self.moxa_ip_label = QLabel("Moxa IP")
        self.moxa_ip_layout.addWidget(self.moxa_ip_label)

        self.moxa_ip = QLineEdit("192.168.0.254")
        self.moxa_ip_layout.addWidget(self.moxa_ip)

        self.moxa_widget = MoxaVisual()
        self.right_layout.addWidget(self.moxa_widget)

        self.camera_display = CameraDisplay(self)
        self.right_layout.addWidget(self.camera_display)

        self.cv_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.cv_thread)
        self.cv_thread.started.connect(self.worker.run)
        # self.signal_send_size_to_worker.connect(self.worker.set_widget_size)

        self.worker.change_pixmap.connect(self.set_image)
        self.cv_thread.start()

        self.right_layout.addStretch()

    @pyqtSlot(QImage)
    def set_image(self, image: QImage):
        self.camera_display.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.cv_thread.requestInterruption()
        self.cv_thread.quit()
        self.hide()
        if self.cv_thread.isRunning():
            self.cv_thread.wait()
        event.accept()
        QApplication.quit()
