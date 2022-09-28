from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLCDNumber, QLabel


class LCDNumber(QLCDNumber):
    def __init__(self, *args, **kwargs):
        super(LCDNumber, self).__init__(*args, **kwargs)
        self.setMaximumWidth(500)
        self.setMaximumHeight(300)
        self.setStyleSheet("QLCDNumber { background-color: black; color: black;}")
        self.setDigitCount(7)

    def reset(self):
        self.display(0)
        self.setStyleSheet("QLCDNumber { background-color: green; color: yellow;}")

    def default(self):
        self.setStyleSheet("QLCDNumber { background-color: white; color: black;}")

    def overLoad(self):
        self.setStyleSheet("QLCDNumber { background-color: red; color: white;}")


class PushBut(QPushButton):
    def __init__(self, *args, **kwargs):
        super(PushBut, self).__init__(*args, **kwargs)

        self.setMouseTracking(True)
        self.setStyleSheet(
            "margin: 1px; padding: 7px; background-color:rgba(125,125,125,100); color: black; border-style: "
            "solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
        )
        self.setMaximumWidth(1000)
        self.setMaximumHeight(50)
        self.setIconSize(QSize(50, 50))

    def enterEvent(self, event):
        if self.isEnabled() is True:
            self.setStyleSheet(
                "margin: 1px; padding: 7px; background-color:rgba(255,255,255,255) ; color: black; "
                "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
            )
        if self.isEnabled() is False:
            pass
            # self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(255,255,255,255);
            # color: black; border-style: solid;border-radius: 3px;border-width: 0.5px;border-color: black;")

    def leaveEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(
                "margin: 1px; padding: 7px; background-color:rgba(125,125,125,100); color: black; "
                "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
            )


class JogBut(QPushButton):
    def __init__(self, *args, **kwargs):
        super(JogBut, self).__init__(*args, **kwargs)

        self.setMouseTracking(True)
        self.setStyleSheet(
            "margin: 1px; padding: 7px; background-color:rgba(125,125,125,100); color: black; "
            "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
        )
        self.setAutoRepeat(True)
        self.setAutoRepeatInterval(30)
        self.setAutoRepeatDelay(0)

    def enterEvent(self, event):
        if self.isEnabled() is True:
            self.setStyleSheet(
                "margin: 1px; padding: 7px; background-color:rgba(255,255,255,255) ; color: black; "
                "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
            )
        if self.isEnabled() is False:
            # self.setStyleSheet("margin: 1px; padding: 7px; background-color: rgba(255,255,255,255);
            # color: black; border-style: solid;border-radius: 3px;border-width: 0.5px;border-color: black;")
            pass

    def leaveEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(
                "margin: 1px; padding: 7px; background-color:rgba(125,125,125,100); color: black; "
                "border-style: solid; border-radius: 3px; border-width: 0.5px; border-color: black;"
            )


class Label(QLabel):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setMaximumWidth(200)
        self.setFixedHeight(30)
        font_label = QFont()
        font_label.setFamily("Helvetica")
        font_label.setPointSize(10)
        font_label.setWeight(25)
        self.setFont(font_label)
        self.setAlignment(Qt.AlignCenter)


class OutputButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(OutputButton, self).__init__(*args, **kwargs)
        self.setStyleSheet("background-color:rgb(200,200,200)")
        self.clicked.connect(self.colorchange)

    def colorchange(self):
        if self.isChecked():
            self.setStyleSheet("background-color:rgb(0,255,0)")
        else:
            self.setStyleSheet("background-color:rgb(200,200,200)")
