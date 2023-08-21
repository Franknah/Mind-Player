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

from qfluentwidgets import (DropDownToolButton, PrimaryPushButton, PushButton, Slider,
    SubtitleLabel, ToggleButton, ToolButton, TransparentDropDownToolButton,
    TransparentPushButton, TransparentToolButton)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(549, 366)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_lyric = SubtitleLabel(Form)
        self.label_lyric.setObjectName(u"label_lyric")
        self.label_lyric.setStyleSheet(u"")
        self.label_lyric.setFrameShape(QFrame.NoFrame)
        self.label_lyric.setFrameShadow(QFrame.Plain)
        self.label_lyric.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_lyric)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.labelLeft = QLabel(Form)
        self.labelLeft.setObjectName(u"labelLeft")
        self.labelLeft.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.labelLeft, 2, 2, 1, 1, Qt.AlignRight)

        self.labelRight = QLabel(Form)
        self.labelRight.setObjectName(u"labelRight")

        self.gridLayout_3.addWidget(self.labelRight, 2, 4, 1, 1, Qt.AlignLeft)

        self.horizontalSlider = Slider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximumSize(QSize(900, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.horizontalSlider, 2, 3, 1, 1)

        self.labelTitle = SubtitleLabel(Form)
        self.labelTitle.setObjectName(u"labelTitle")
        font = QFont()
        font.setBold(True)
        self.labelTitle.setFont(font)

        self.gridLayout_3.addWidget(self.labelTitle, 0, 2, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonPast = PrimaryPushButton(Form)
        self.pushButtonPast.setObjectName(u"pushButtonPast")

        self.horizontalLayout.addWidget(self.pushButtonPast, 0, Qt.AlignRight)

        self.pushButton = ToggleButton(Form)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButtonNext = PrimaryPushButton(Form)
        self.pushButtonNext.setObjectName(u"pushButtonNext")

        self.horizontalLayout.addWidget(self.pushButtonNext, 0, Qt.AlignLeft)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButtonDtLrc = TransparentToolButton(Form)
        self.toolButtonDtLrc.setObjectName(u"toolButtonDtLrc")
        self.toolButtonDtLrc.setPopupMode(QToolButton.DelayedPopup)

        self.horizontalLayout_2.addWidget(self.toolButtonDtLrc)

        self.toolButtonVolumn = TransparentToolButton(Form)
        self.toolButtonVolumn.setObjectName(u"toolButtonVolumn")
        self.toolButtonVolumn.setAutoRaise(False)

        self.horizontalLayout_2.addWidget(self.toolButtonVolumn)

        self.toolButtonPlayMode = TransparentDropDownToolButton(Form)
        self.toolButtonPlayMode.setObjectName(u"toolButtonPlayMode")

        self.horizontalLayout_2.addWidget(self.toolButtonPlayMode)


        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 6, 1, 1)

        self.pushButtonLyric = TransparentPushButton(Form)
        self.pushButtonLyric.setObjectName(u"pushButtonLyric")

        self.gridLayout.addWidget(self.pushButtonLyric, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_lyric.setText("")
        self.labelLeft.setText(QCoreApplication.translate("Form", u"0\uff1a00", None))
        self.labelRight.setText(QCoreApplication.translate("Form", u"0\uff1a00", None))
        self.labelTitle.setText("")
        self.pushButtonPast.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u9996", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u64ad\u653e", None))
        self.pushButtonNext.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u9996", None))
        self.toolButtonVolumn.setText("")
        self.toolButtonPlayMode.setText("")
        self.pushButtonLyric.setText(QCoreApplication.translate("Form", u"\u5207\u6362\u6b4c\u8bcd", None))
    # retranslateUi

