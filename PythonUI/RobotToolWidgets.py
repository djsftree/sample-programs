from pathlib import Path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFontMetricsF
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QRadioButton,
    QPlainTextEdit,
    QVBoxLayout,
    QSlider,
    QLineEdit,
    QFrame,
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkAssembly, vtkCamera
from PyQt5Widgets import PushBut, LCDNumber, Label, JogBut, OutputButton
from vtkmeca500 import load_STL, create_coordinates, create_ground


class PoseWidget(QWidget):
    def __init__(self, names: list[str]):
        super(PoseWidget, self).__init__()

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.lcd_1 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_1, 0, 0)

        self.lcd_2 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_2, 0, 1)

        self.lcd_3 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_3, 0, 2)

        self.lcd_4 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_4, 0, 3)

        self.lcd_5 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_5, 0, 4)

        self.lcd_6 = LCDNumber()
        self.gridLayout.addWidget(self.lcd_6, 0, 5)

        self.label_1 = Label(names[0])
        self.gridLayout.addWidget(self.label_1, 1, 0)

        self.label_2 = Label(names[1])
        self.gridLayout.addWidget(self.label_2, 1, 1)

        self.label_3 = Label(names[2])
        self.gridLayout.addWidget(self.label_3, 1, 2)

        self.label_4 = Label(names[3])
        self.gridLayout.addWidget(self.label_4, 1, 3)

        self.label_5 = Label(names[4])
        self.gridLayout.addWidget(self.label_5, 1, 4)

        self.label_6 = Label(names[5])
        self.gridLayout.addWidget(self.label_6, 1, 5)

    def update_lcd(self, info):
        self.lcd_1.display(info[0])
        self.lcd_2.display(info[1])
        self.lcd_3.display(info[2])
        self.lcd_4.display(info[3])
        self.lcd_5.display(info[4])
        self.lcd_6.display(info[5])

    def reset(self):
        self.lcd_1.display(0)
        self.lcd_1.default()
        self.lcd_2.display(0)
        self.lcd_2.default()
        self.lcd_3.display(0)
        self.lcd_3.default()
        self.lcd_4.display(0)
        self.lcd_4.default()
        self.lcd_5.display(0)
        self.lcd_5.default()
        self.lcd_6.display(0)
        self.lcd_6.default()


class JogPanel(QWidget):
    mode = pyqtSignal(str)
    vel = pyqtSignal(int)
    delta = pyqtSignal(list)

    def __init__(self, parent=None):
        super(JogPanel, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.jogging_mode_button = QPushButton("Jogging Mode")
        self.jogging_mode_button.setMaximumHeight(50)
        self.jogging_mode_button.clicked.connect(self.enable_jog)
        self.main_layout.addWidget(self.jogging_mode_button)

        self.joymode_button = QPushButton("Use Joystick")
        self.joymode_button.setMaximumHeight(25)
        self.joymode_button.setEnabled(False)
        self.joymode_button.clicked.connect(self.on_joy_mode)
        self.main_layout.addWidget(self.joymode_button)

        self.radio_buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.radio_buttons_layout)

        self.joints_mode = QRadioButton("Joints")
        self.radio_buttons_layout.addWidget(self.joints_mode)
        self.joints_mode.toggled.connect(self.on_joints)

        self.wrf_mode = QRadioButton("WRF")
        self.radio_buttons_layout.addWidget(self.wrf_mode)
        self.wrf_mode.toggled.connect(self.on_WRF)

        self.trf_mode = QRadioButton("TRF")
        self.radio_buttons_layout.addWidget(self.trf_mode)
        self.trf_mode.toggled.connect(self.on_TRF)

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.label_1 = QLabel()
        self.grid_layout.addWidget(self.label_1, 0, 0)

        self.btn1 = JogBut("-")
        self.grid_layout.addWidget(self.btn1, 0, 1)

        self.btn2 = JogBut("+")
        self.grid_layout.addWidget(self.btn2, 0, 2)

        self.label_2 = QLabel()
        self.grid_layout.addWidget(self.label_2, 1, 0)

        self.btn3 = JogBut("-")
        self.grid_layout.addWidget(self.btn3, 1, 1)

        self.btn4 = JogBut("+")
        self.grid_layout.addWidget(self.btn4, 1, 2)

        self.label_3 = QLabel()
        self.grid_layout.addWidget(self.label_3, 2, 0)

        self.btn5 = JogBut("-")
        self.grid_layout.addWidget(self.btn5, 2, 1)

        self.btn6 = JogBut("+")
        self.grid_layout.addWidget(self.btn6, 2, 2)

        self.label_4 = QLabel()
        self.grid_layout.addWidget(self.label_4, 3, 0)

        self.btn7 = JogBut("-")
        self.grid_layout.addWidget(self.btn7, 3, 1)

        self.btn8 = JogBut("+")
        self.grid_layout.addWidget(self.btn8, 3, 2)

        self.label_5 = QLabel()
        self.grid_layout.addWidget(self.label_5, 4, 0)

        self.btn9 = JogBut("-")
        self.grid_layout.addWidget(self.btn9, 4, 1)

        self.btn10 = JogBut("+")
        self.grid_layout.addWidget(self.btn10, 4, 2)

        self.label_6 = QLabel()
        self.grid_layout.addWidget(self.label_6, 5, 0)

        self.btn11 = JogBut("-")
        self.grid_layout.addWidget(self.btn11, 5, 1)

        self.btn12 = JogBut("+")
        self.grid_layout.addWidget(self.btn12, 5, 2)

        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn4.setEnabled(False)
        self.btn5.setEnabled(False)
        self.btn6.setEnabled(False)
        self.btn7.setEnabled(False)
        self.btn8.setEnabled(False)
        self.btn9.setEnabled(False)
        self.btn10.setEnabled(False)
        self.btn11.setEnabled(False)
        self.btn12.setEnabled(False)

        self.speed_set_label = QLabel("Speed Settings")
        self.main_layout.addWidget(self.speed_set_label)

        self.slider_layout = QHBoxLayout()
        self.main_layout.addLayout(self.slider_layout)

        self.speed = QSlider(Qt.Horizontal)
        self.speed.setRange(0, 20)
        self.speed.setFocusPolicy(Qt.NoFocus)
        self.speed.setPageStep(5)
        self.speed.setValue(0)
        self.speed.valueChanged.connect(self.updateVal)
        self.slider_layout.addWidget(self.speed)

        self.value_label = QLabel("0")
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.slider_layout.addWidget(self.value_label)

        # Button connection
        self.btn1.clicked.connect(lambda ignore, label=0, direction="-": self.on_button_delta(label, direction))
        self.btn2.clicked.connect(lambda ignore, label=0, direction="+": self.on_button_delta(label, direction))
        self.btn3.clicked.connect(lambda ignore, label=1, direction="-": self.on_button_delta(label, direction))
        self.btn4.clicked.connect(lambda ignore, label=1, direction="+": self.on_button_delta(label, direction))
        self.btn5.clicked.connect(lambda ignore, label=2, direction="-": self.on_button_delta(label, direction))
        self.btn6.clicked.connect(lambda ignore, label=2, direction="+": self.on_button_delta(label, direction))
        self.btn7.clicked.connect(lambda ignore, label=3, direction="-": self.on_button_delta(label, direction))
        self.btn8.clicked.connect(lambda ignore, label=3, direction="+": self.on_button_delta(label, direction))
        self.btn9.clicked.connect(lambda ignore, label=4, direction="-": self.on_button_delta(label, direction))
        self.btn10.clicked.connect(lambda ignore, label=4, direction="+": self.on_button_delta(label, direction))
        self.btn11.clicked.connect(lambda ignore, label=5, direction="-": self.on_button_delta(label, direction))
        self.btn12.clicked.connect(lambda ignore, label=5, direction="+": self.on_button_delta(label, direction))

        self.main_layout.addStretch()

    def enable_jog(self):
        if self.jogging_mode_button.isChecked():

            self.joints_mode.setEnabled(True)
            self.wrf_mode.setEnabled(True)
            self.trf_mode.setEnabled(True)
            self.joymode_button.setEnabled(True)

            self.btn1.setEnabled(True)
            self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)
            self.btn4.setEnabled(True)
            self.btn5.setEnabled(True)
            self.btn6.setEnabled(True)
            self.btn7.setEnabled(True)
            self.btn8.setEnabled(True)
            self.btn9.setEnabled(True)
            self.btn10.setEnabled(True)
            self.btn11.setEnabled(True)
            self.btn12.setEnabled(True)
        else:
            self.joints_mode.setEnabled(False)
            self.wrf_mode.setEnabled(False)
            self.trf_mode.setEnabled(False)
            self.joymode_button.setEnabled(False)

            self.btn1.setEnabled(False)
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(False)
            self.btn4.setEnabled(False)
            self.btn5.setEnabled(False)
            self.btn6.setEnabled(False)
            self.btn7.setEnabled(False)
            self.btn8.setEnabled(False)
            self.btn9.setEnabled(False)
            self.btn10.setEnabled(False)
            self.btn11.setEnabled(False)
            self.btn12.setEnabled(False)

    def on_joy_mode(self):
        if self.joymode_button.isChecked():
            self.btn1.setEnabled(False)
            self.btn2.setEnabled(False)
            self.btn3.setEnabled(False)
            self.btn4.setEnabled(False)
            self.btn5.setEnabled(False)
            self.btn6.setEnabled(False)
            self.btn7.setEnabled(False)
            self.btn8.setEnabled(False)
            self.btn9.setEnabled(False)
            self.btn10.setEnabled(False)
            self.btn11.setEnabled(False)
            self.btn12.setEnabled(False)
        else:
            self.btn1.setEnabled(True)
            self.btn2.setEnabled(True)
            self.btn3.setEnabled(True)
            self.btn4.setEnabled(True)
            self.btn5.setEnabled(True)
            self.btn6.setEnabled(True)
            self.btn7.setEnabled(True)
            self.btn8.setEnabled(True)
            self.btn9.setEnabled(True)
            self.btn10.setEnabled(True)
            self.btn11.setEnabled(True)
            self.btn12.setEnabled(True)

    def on_joints(self):
        self.mode.emit("Joints")
        self.updateLabel("Joints")

    def on_WRF(self):
        self.mode.emit("WRF")
        self.updateLabel("WRF")

    def on_TRF(self):
        self.mode.emit("TRF")
        self.updateLabel("TRF")

    def updateLabel(self, value):
        if value == "Joints":
            self.label_1.setText("J1")
            self.label_2.setText("J2")
            self.label_3.setText("J3")
            self.label_4.setText("J4")
            self.label_5.setText("J5")
            self.label_6.setText("J6")

        elif value in ("WRF", "TRF"):
            self.label_1.setText("X")
            self.label_2.setText("Y")
            self.label_3.setText("Z")
            self.label_4.setText("Rx")
            self.label_5.setText("Ry")
            self.label_6.setText("Rz")

    def updateVal(self, value):
        self.value_label.setText(str(value))
        self.vel.emit(value)

    def on_button_delta(self, label, direction):
        data = [0, 0, 0, 0, 0, 0]
        if direction == "+":
            data[label] = 1
        else:
            data[label] = -1
        self.delta.emit(data)


class MyInteractor(vtkInteractorStyleTrackballCamera):
    def __init__(self):
        vtkInteractorStyleTrackballCamera.__init__(self)

        self.AddObserver("CharEvent", self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        return


class Slider(QSlider):
    def __init__(self):
        QSlider.__init__(self)

        self.setMinimum(-175)
        self.setMaximum(175)
        self.setValue(0)
        self.setOrientation(Qt.Horizontal)


class TeachPanel(QWidget):
    def __init__(self, window):
        super(TeachPanel, self).__init__()

        self.window = window

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.command_lineedit = QLineEdit()
        self.command_lineedit.setPlaceholderText("Command to send...")
        self.command_lineedit.setStyleSheet(
            "margin: 1px; padding: 7px;border-style: solid;border-radius: 3px;border-width: 0.5px;"
        )
        self.main_layout.addWidget(self.command_lineedit)

        self.send_button = PushBut()
        self.send_button.setText("Send")
        self.main_layout.addWidget(self.send_button)

        self.program = QPlainTextEdit()
        self.program.setPlaceholderText("Programm...")
        self.program.setTabStopDistance(QFontMetricsF(self.program.font()).horizontalAdvance(" ") * 4)
        self.main_layout.addWidget(self.program)

        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout)

        self.move_joints_button = PushBut("MoveJoints")
        self.buttons_layout.addWidget(self.move_joints_button)

        self.move_pose_button = PushBut("MovePose")
        self.buttons_layout.addWidget(self.move_pose_button)

        self.move_lin_button = PushBut("MoveLin")
        self.buttons_layout.addWidget(self.move_lin_button)

        self.frame = QFrame()
        self.vtk_widget = QVTKRenderWindowInteractor(self.frame)
        self.main_layout.addWidget(self.vtk_widget)

        self.main_layout.addStretch()

        self.renderer = vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        self.style = MyInteractor()
        self.style.SetDefaultRenderer(self.renderer)
        self.interactor.SetInteractorStyle(self.style)

        filenames = [
            "meca500_base.stl",
            "link1.stl",
            "link2.stl",
            "link3.stl",
            "link4.stl",
            "link5.stl",
            "link6.stl",
            "spindle_assy.stl",
        ]
        filenames = ["stl" / Path(filename) for filename in filenames]

        self.actor = []
        self.meca500_assy = []
        for actor_id, file in enumerate(filenames):
            self.actor.append(load_STL(file))
            self.actor[actor_id].GetProperty().SetDiffuseColor(0.9, 0.9, 0.9)
            self.actor[actor_id].GetProperty().SetDiffuse(0.8)
            self.actor[actor_id].GetProperty().SetSpecular(0.5)
            self.actor[actor_id].GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
            self.actor[actor_id].GetProperty().SetSpecularPower(30.0)

            tmp_assembly = vtkAssembly()
            tmp_assembly.SetObjectName(f"Assembly_{file}")
            self.meca500_assy.append(tmp_assembly)
            self.meca500_assy[actor_id].AddPart(self.actor[actor_id])

            if actor_id > 0:
                self.meca500_assy[actor_id - 1].AddPart(tmp_assembly)

        self.meca500_assy[0].SetOrigin(0, 0, 0)
        self.meca500_assy[1].SetOrigin(0, 0, 135)
        self.meca500_assy[2].SetOrigin(0, 0, 135)
        self.meca500_assy[3].SetOrigin(135, 0, 135)
        self.meca500_assy[4].SetOrigin(173, 0, 50)
        self.meca500_assy[5].SetOrigin(173, 0, 15)
        self.meca500_assy[6].SetOrigin(173, 0, -55)

        self.meca500_assy[0].SetPosition(0, 0, 0)
        self.meca500_assy[1].SetPosition(0, 0, 0)
        self.meca500_assy[2].SetPosition(0, 0, 0)
        self.meca500_assy[3].SetPosition(0, 0, 0)
        self.meca500_assy[4].SetPosition(0, 0, 0)
        self.meca500_assy[5].SetPosition(0, 0, 0)
        self.meca500_assy[6].SetPosition(0, 0, 0)

        self.renderer.AddActor(self.meca500_assy[0])

        # Add coordinates
        axes = create_coordinates()
        self.renderer.AddActor(axes)

        # Add ground
        ground = create_ground()
        self.renderer.AddActor(ground)

        self.renderer.SetBackground(0.2, 0.2, 0.2)

        self.camera = vtkCamera()
        self.camera.SetFocalPoint(150, 0, 0)
        self.camera.SetPosition(400, 100, 400)
        self.camera.ComputeViewPlaneNormal()
        self.camera.SetViewUp(0, 0, 1)
        self.camera.Zoom(0.3)
        self.renderer.SetActiveCamera(self.camera)

        self.interactor.Initialize()

    def set_orientation(self, meca_index: int, position: int):
        if meca_index == 1:
            self.meca500_assy[meca_index].SetOrientation(0, 0, position)
            self.window.slider_1.setValue(position)
            self.window.joint_pose.lcd_1.display(position)
        elif meca_index == 2:
            self.meca500_assy[meca_index].SetOrientation(0, position, 0)
            self.window.slider_2.setValue(position)
            self.window.joint_pose.lcd_2.display(position)
        elif meca_index == 3:
            self.meca500_assy[meca_index].SetOrientation(0, position, 0)
            self.window.slider_3.setValue(position)
            self.window.joint_pose.lcd_3.display(position)
        elif meca_index == 4:
            self.meca500_assy[meca_index].SetOrientation(0, 0, position)
            self.window.slider_4.setValue(position)
            self.window.joint_pose.lcd_4.display(position)
        elif meca_index == 5:
            self.meca500_assy[meca_index].SetOrientation(0, -position, 0)
            self.window.slider_5.setValue(position)
            self.window.joint_pose.lcd_5.display(position)
        elif meca_index == 6:
            self.meca500_assy[meca_index].SetOrientation(0, 0, -position)
            self.window.slider_6.setValue(position)
            self.window.joint_pose.lcd_6.display(position)
        else:
            raise Exception("Unknown index")
        # Update the view
        self.interactor.Render()


class MoxaVisual(QWidget):
    def __init__(self):
        super(MoxaVisual, self).__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.Inputs = QVBoxLayout()
        self.Outputs = QVBoxLayout()
        self.OutLabels = QVBoxLayout()

        self.main_layout.addLayout(self.Inputs)
        self.main_layout.addLayout(self.OutLabels)
        self.main_layout.addLayout(self.Outputs)

        self.in_0 = QLabel("Input 0")
        self.in_1 = QLabel("Input 1")
        self.in_2 = QLabel("Input 2")
        self.in_3 = QLabel("Input 3")
        self.in_4 = QLabel("Input 4")
        self.in_5 = QLabel("Input 5")
        self.in_6 = QLabel("Input 6")
        self.in_7 = QLabel("Input 7")
        self.in_0.setStyleSheet("border: 1px solid black;")
        self.in_1.setStyleSheet("border: 1px solid black;")
        self.in_2.setStyleSheet("border: 1px solid black;")
        self.in_3.setStyleSheet("border: 1px solid black;")
        self.in_4.setStyleSheet("border: 1px solid black;")
        self.in_5.setStyleSheet("border: 1px solid black;")
        self.in_6.setStyleSheet("border: 1px solid black;")
        self.in_7.setStyleSheet("border: 1px solid black;")

        self.outL_0 = QLabel("Output 0")
        self.outL_1 = QLabel("Output 1")
        self.outL_2 = QLabel("Output 2")
        self.outL_3 = QLabel("Output 3")
        self.outL_4 = QLabel("Output 4")
        self.outL_5 = QLabel("Output 5")
        self.outL_6 = QLabel("Output 6")
        self.outL_7 = QLabel("Output 7")

        self.out_0 = OutputButton()
        self.out_1 = OutputButton()
        self.out_2 = OutputButton()
        self.out_3 = OutputButton()
        self.out_4 = OutputButton()
        self.out_5 = OutputButton()
        self.out_6 = OutputButton()
        self.out_7 = OutputButton()

        self.Inputs.addWidget(self.in_0)
        self.Inputs.addWidget(self.in_1)
        self.Inputs.addWidget(self.in_2)
        self.Inputs.addWidget(self.in_3)
        self.Inputs.addWidget(self.in_4)
        self.Inputs.addWidget(self.in_5)
        self.Inputs.addWidget(self.in_6)
        self.Inputs.addWidget(self.in_7)

        self.OutLabels.addWidget(self.outL_0)
        self.OutLabels.addWidget(self.outL_1)
        self.OutLabels.addWidget(self.outL_2)
        self.OutLabels.addWidget(self.outL_3)
        self.OutLabels.addWidget(self.outL_4)
        self.OutLabels.addWidget(self.outL_5)
        self.OutLabels.addWidget(self.outL_6)
        self.OutLabels.addWidget(self.outL_7)

        self.Outputs.addWidget(self.out_0)
        self.Outputs.addWidget(self.out_1)
        self.Outputs.addWidget(self.out_2)
        self.Outputs.addWidget(self.out_3)
        self.Outputs.addWidget(self.out_4)
        self.Outputs.addWidget(self.out_5)
        self.Outputs.addWidget(self.out_6)
        self.Outputs.addWidget(self.out_7)

    def update_input(self, values):
        color_high = "background-color:rgb(0,255,0)"
        color_low = "background-color:rgb(200,200,200)"
        if values[0]:
            self.in_0.setStyleSheet(color_high)
        else:
            self.in_0.setStyleSheet(color_low)
        if values[1]:
            self.in_1.setStyleSheet(color_high)
        else:
            self.in_1.setStyleSheet(color_low)
        if values[2]:
            self.in_2.setStyleSheet(color_high)
        else:
            self.in_2.setStyleSheet(color_low)
        if values[3]:
            self.in_3.setStyleSheet(color_high)
        else:
            self.in_3.setStyleSheet(color_low)
        if values[4]:
            self.in_4.setStyleSheet(color_high)
        else:
            self.in_4.setStyleSheet(color_low)
        if values[5]:
            self.in_5.setStyleSheet(color_high)
        else:
            self.in_5.setStyleSheet(color_low)
        if values[6]:
            self.in_6.setStyleSheet(color_high)
        else:
            self.in_6.setStyleSheet(color_low)
        if values[7]:
            self.in_7.setStyleSheet(color_high)
        else:
            self.in_7.setStyleSheet(color_low)
