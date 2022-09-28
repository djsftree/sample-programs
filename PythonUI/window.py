from PyQt5.QtCore import Qt
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
)

from RobotToolWidgets import JogPanel, MoxaVisual, PoseWidget, TeachPanel


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Mecademic Robot")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        self.jog_widget = JogPanel()
        self.central_layout.addWidget(self.jog_widget)

        self.mid_layout = QVBoxLayout()
        self.central_layout.addLayout(self.mid_layout)

        self.joint_pose = PoseWidget()
        self.mid_layout.addWidget(self.joint_pose)

        self.tcp_pose = PoseWidget()
        self.mid_layout.addWidget(self.tcp_pose)

        self.teach_window = TeachPanel()
        self.mid_layout.addWidget(self.teach_window)

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

        self.right_layout.addStretch()
