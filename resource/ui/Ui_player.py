# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'player.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QSizePolicy, QToolButton,
    QVBoxLayout, QWidget)

from qfluentwidgets import (PrimaryPushButton, Slider,TransparentDropDownToolButton, ToggleButton,
    TransparentToggleToolButton,BodyLabel,SubtitleLabel,TitleLabel,LargeTitleLabel)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(549, 363)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_lyric = SubtitleLabel(Form)
        self.label_lyric.setObjectName(u"label_lyric")

        self.label_lyric.setFrameShape(QFrame.NoFrame)
        self.label_lyric.setFrameShadow(QFrame.Plain)
        self.label_lyric.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_lyric)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSlider = Slider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximumSize(QSize(900, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider, 2, 3, 1, 1)

        self.labelTitle = SubtitleLabel(Form)
        self.labelTitle.setObjectName(u"labelTitle")


        self.gridLayout_3.addWidget(self.labelTitle, 0, 2, 1, 3)

        self.label = BodyLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.label, 2, 2, 1, 1, Qt.AlignRight)

        self.label_2 = BodyLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 2, 4, 1, 1, Qt.AlignLeft)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolButton_3 = TransparentToggleToolButton(Form)
        self.toolButton_3.setObjectName(u"toolButton_3")
        self.toolButton_3.setAutoRaise(False)
        self.toolButton_3.setCheckable(False)
        self.gridLayout.addWidget(self.toolButton_3, 1, 2, 1, 1, Qt.AlignRight)

        self.toolButton_2 =TransparentDropDownToolButton(Form)
        self.toolButton_2.setObjectName(u"toolButton_2")

        self.gridLayout.addWidget(self.toolButton_2, 1, 3, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonPast = PrimaryPushButton(Form)
        self.pushButtonPast.setObjectName(u"pushButtonPast")

        self.horizontalLayout.addWidget(self.pushButtonPast, 0, Qt.AlignRight)

        self.pushButton = ToggleButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMaximumSize(QSize(139, 16777215))


        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButtonNext = PrimaryPushButton(Form)
        self.pushButtonNext.setObjectName(u"pushButtonNext")

        self.horizontalLayout.addWidget(self.pushButtonNext, 0, Qt.AlignLeft)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 4)

        self.toolButton = TransparentToggleToolButton(Form)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setCheckable(False)
        self.toolButton.setAutoRepeat(False)
        self.toolButton.setAutoExclusive(False)
        self.toolButton.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolButton.setAutoRaise(True)

        self.gridLayout.addWidget(self.toolButton, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_lyric.setText("")
        self.labelTitle.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"0\uff1a00", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"0\uff1a00", None))
        self.toolButton_3.setText("")
        self.pushButtonPast.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u9996", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u64ad\u653e", None))
        self.pushButtonNext.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u9996", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"\u5207\u6362\u6b4c\u8bcd", None))
    # retranslateUi

