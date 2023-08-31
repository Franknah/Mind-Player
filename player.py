from math import floor
import enum
import sys
import re
import os
import io
from typing import Optional
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Slot, QSignalBlocker, Qt, Signal
from PySide6.QtGui import QPixmap, QAction, QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QFrame,
                               QFileDialog, QVBoxLayout, QLabel)
# from PySide6.QtMultimedia import QMediaFormat
from resource.ui.player_ui import Ui_Form
from qfluentwidgets import (isDarkTheme, setTheme, RoundMenu, InfoBar,
                            InfoBarPosition, Theme, FluentIcon as FiF,
                            FlyoutViewBase, Flyout, FlyoutAnimationType,
                            Slider, Action, ToolTipFilter,FluentIconBase)
from Parser import Lyric
from config import cfg


class PlayMode(enum.Enum):
    '''
    顺序播放
    随机播放
    列表循环
    单曲循环
    '''
    order = 0
    random = 1
    repeat = 2
    single = 3

class PIF(FluentIconBase,enum.Enum):
    # Private Icon
    order = "play in order"
    random = "random"
    repeat = "repeat"
    single= "single repeat"
    sound = "sound"
    soundEmpty="sound empty"
    lyric = "lyric"
    def path(self,theme=cfg.theme):
        color = "dark" if isDarkTheme() else "light"
        return f"resource/icon/{self.value}-{color}.svg"
    
class MyAudioPlayer(QWidget, Ui_Form):
    '''播放页'''
    modeChanged = Signal()
    lyricChanged = Signal()
    def __init__(self):
        super().__init__()
        # self.fp =r"resource\たぶん-YOASOBI.mp3"
        # self.lyricPath=r"resource\たぶん-YOASOBI.lrc"
        self.fp, self.lyricPath, self.isplay = "", "", True
        self.setObjectName("Player")
        self.setupUi(self)
        self.player = QMediaPlayer()
        self.playMode = PlayMode.order
        self.slider.setValue(0)
        self.audioOutput = QAudioOutput()  # 不能实例化为临时变量，否则被自动回收导致无法播放
        self.player.setAudioOutput(self.audioOutput)
        self.block = QSignalBlocker(self.player)
        self.block.unblock()
        self.menu = RoundMenu(parent=self)
        self.createMenu()
        self.volumnSlider = Slider(Qt.Orientation.Horizontal)
        self.volumnSlider.setRange(0, 100)
        self.volumnSlider.setValue(100)
        self.setQss()

        self.switchMode(PlayMode.order)
        self.shareSignal()
        self.initWindow()

    def shareSignal(self):
        cfg.themeChanged.connect(self.__onThemeChanged)
        self.pushButton.clicked.connect(self.StateInit)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.slider.sliderMoved.connect(self.dragSlider)
        self.slider.clicked.connect(self.clickSlider)
        self.slider.sliderReleased.connect(self.releaseSlider)
        self.pushButtonSwitch.clicked.connect(self.changeLyric)
        self.toolButtonVolumn.clicked.connect(lambda: Flyout.make(CustomFlyoutView(
            self), self.toolButtonVolumn, self, FlyoutAnimationType.PULL_UP))

    def initWindow(self):
        self.lyric_dict = Lyric(self.lyricPath)


    def show_lyric(self, position: int):
        # 查找对应的歌词并显示在标签上
        text = self.lyric_dict.getLyric(position)
        self.label_lyric.setText(text)
        self.lyricChanged.emit()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{color}/player.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        self.switchMode(self.playMode)
        if self.volumnSlider.value() == 0:
            self.toolButtonVolumn.setIcon(PIF.soundEmpty)
        else:
            self.toolButtonVolumn.setIcon(PIF.sound)
        self.toolButtonDtLrc.setIcon(PIF.lyric)

    def createMenu(self):
        color = 'dark' if isDarkTheme() else 'light'
        self.action1 = Action(PIF.order,
                              "顺序播放", self,
                              triggered=lambda: self.switchMode(PlayMode.order))
        self.action2 = Action(PIF.random,
                              "随机播放", self,
                              triggered=lambda: self.switchMode(PlayMode.random))
        self.action3 = Action(PIF.repeat,
                              "列表循环", self,
                              triggered=lambda: self.switchMode(PlayMode.repeat))
        self.action4 = Action(PIF.single,
                              "单曲循环", self,
                              triggered=lambda: self.switchMode(PlayMode.single))

        self.actions = [
            self.action1,
            self.action2,
            self.action3,
            self.action4
        ]
        self.menu.addActions(self.actions)
        self.toolButtonPlayMode.setMenu(self.menu)

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)
        self.setQss()

    def switchSong(self, file: str, info: list, itemIndex: int):
        '''切换歌曲'''
        try:
            self.isplay = True
            self.fp = os.path.normpath(file)
            self.player.setSource(QUrl.fromLocalFile(self.fp))
            self.initWindow()
            self.lyricSetting()
            self.labelTitle.setText(info[0]+"-"+info[1])
            self.setPlayState(QMediaPlayer.PlaybackState.PlayingState)
        except FileNotFoundError:
            InfoBar.error("错误", f"找不到文件'{file}'", parent=self)

        except PermissionError:
            InfoBar.error("权限错误", "没有足够的权限", parent=self)

    def lyricSetting(self):
        if self.fp in cfg.lyricFolders.value:
            self.label_lyric.setText("")
            self.lyricPath = os.path.normpath(cfg.lyricFolders.value[self.fp])
        else:
            self.lyricPath = ""
        self.lyric_dict.path = self.lyricPath

    def switchMode(self, mode: PlayMode):
        '''切换播放模式'''
        self.playMode = mode
        self.toolButtonPlayMode.setIcon(self.actions[mode.value].icon())
        if mode == PlayMode.order:
            self.toolButtonPlayMode.setToolTip("顺序播放")
        elif mode == PlayMode.random:
            self.toolButtonPlayMode.setToolTip("随机播放")
        elif mode == PlayMode.repeat:
            self.toolButtonPlayMode.setToolTip("列表循环")
        elif mode == PlayMode.single:
            self.toolButtonPlayMode.setToolTip("单曲循环")
        self.modeChanged.emit()
    @Slot()
    def StateInit(self):
        if self.fp == "":
            InfoBar.error("错误", "没有添加媒体",
                          position=InfoBarPosition.TOP, parent=self)
        if self.pushButton.isChecked():
            self.pushButton.setIcon(r"resource\icon\play.ico")
            self.pushButton.setText("暂停")
            self.player.play()
            self.isplay = True
        else:
            self.pushButton.setIcon(r"resource\icon\pause.ico")
            self.pushButton.setText("播放")
            self.player.pause()
            self.isplay = True

    def setPlayState(self, state: QMediaPlayer.PlaybackState):
        if state == self.player.PlaybackState.StoppedState:
            self.pushButton.setChecked(False)
            self.pushButton.setIcon(r"resource\icon\stop.ico")
            self.pushButton.setText("播放")
        elif state == self.player.PlaybackState.PlayingState:
            self.pushButton.setChecked(True)
            self.pushButton.setIcon(r"resource\icon\play.ico")
            self.pushButton.setText("暂停")
        elif state == self.player.PlaybackState.PausedState:
            self.pushButton.setChecked(False)
            self.pushButton.setIcon(r"resource\icon\pause.ico")
            self.pushButton.setText("播放")
        self.StateInit()

    @Slot()
    def positionChanged(self, position: int):
        self.updateTime(position)
        max = self.slider.maximum()
        if self.player.duration() != 0:
            value = position/self.player.duration()*max
            self.slider.setValue(value)
            if self.slider.value() == max:
                self.isplay = False
        if self.lyricPath != "":
            self.show_lyric(position)
        else:
            self.label_lyric.setText("暂无歌词")

    def updateTime(self, position: int):
        second = floor((position / 1000) % 60)
        minute = floor((position / (1000 * 60)) % 60)
        self.labelLeft.setText(f"{minute:02d} :{second:02d}")

    @Slot()
    def durationChanged(self, duration):
        second = int((duration / 1000) % 60)
        minute = int((duration / (1000 * 60)) % 60)
        self.slider.setMaximum(int(duration/1000)*2)

        self.labelRight.setText(f"{minute:02d} :{second:02d}")

    @Slot()
    def dragSlider(self):
        self.label_lyric.setText("")
        self.setToolTip("")
        if self.slider.underMouse(): # 解决拖动时仍播放
            self.player.pause()
        else:
            self.player.play()
        # self.player.pause()
        if self.fp == "":
            return
        # self.block.reblock()
        slider = self.slider
        sc = floor(slider.value()/slider.maximum()*self.player.duration())
        if sc == self.player.duration():
            return
        self.player.setPosition(sc)
        self.updateTime(self.player.position())
    @Slot()
    def clickSlider(self):
        if self.fp == "":
            return
        slider = self.slider
        sc = floor(slider.value()/slider.maximum()*self.player.duration())
        self.player.setPosition(sc)
        self.updateTime(self.player.position())
        self.player.play()

    @Slot()
    def releaseSlider(self):
        # self.block.unblock()
        self.setPlayState(QMediaPlayer.PlaybackState.PlayingState)
        # self.positionChanged(self.player.position())

    @Slot()
    def changeLyric(self):
        '''切换歌词'''
        try:
            path, _ = QFileDialog().getOpenFileName(self, 
                                                    "选择歌词文件",
                                                    cfg.musicFolders.value[0], 
                                                    filter="*.lrc")
            if path == "":
                return

            self.lyricPath = os.path.normpath(path)
            self.lyric_dict
            dict = cfg.lyricFolders.value.copy()

            dict[self.fp] = self.lyricPath
            cfg.set(cfg.lyricFolders, dict)

        except PermissionError:
            InfoBar.error("权限错误", "已经被其他程序访问或没有权限打开文件！", parent=self)


class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent: MyAudioPlayer = None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.slider = parent.volumnSlider
        self.slider.setValue(parent.audioOutput.volume()*100)
        self.slider.setMaximum(100)
        self.labelLeft = QLabel(self)
        self.labelLeft.setAlignment(Qt.AlignCenter)
        self.slider.valueChanged.connect(self.changeVolumn)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.slider)

    def changeVolumn(self):
        value = self.slider.value()
        self.parent().parent().audioOutput.setVolume(value/100)
        self.labelLeft.setText("当前音量："+str(self.slider.value()))
        self.parent().parent().setQss()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    audioPlayer = MyAudioPlayer()
    audioPlayer.show()
    sys.exit(app.exec())
