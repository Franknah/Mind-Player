import sys
import random
from qframelesswindow import WindowEffect
from qfluentwidgets import (
    NavigationItemPosition, FluentIcon as FIF, isDarkTheme,
    FluentTranslator, Theme, setTheme, SplashScreen, InfoBar,
    FluentWindow, SystemTrayMenu, Action, toggleTheme)
from PySide6.QtWidgets import QApplication, QTableWidgetItem, QSystemTrayIcon, QMenu
from player import MyAudioPlayer, PlayMode
from list import PlayList
from config import cfg
from PySide6.QtGui import QIcon
from setting_interface import SettingInterface
from PySide6.QtCore import (Qt, QTranslator, Slot, QSize, QTimer, QEventLoop)


class Main(FluentWindow):

    def __init__(self):
        super().__init__()

        self.resize(800, 600)
        self.initWindow()
        self.setSplashScreen()
        self.index = 0
        self.setQss()
        cfg.themeChanged.connect(self.__onThemeChanged)
        self.musicInterface = MyAudioPlayer()
        self.ListInterface = PlayList()
        self.settingInterface = SettingInterface()
        self.shareSignal()
        self.initNavigation()
        self.wscreen.finish()
        self.tray = tray(self)
        self.tray.show()

    def setSplashScreen(self):
        self.wscreen = SplashScreen(self.windowIcon(), self, True)
        self.wscreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()

    def createSubInterface(self):
        # Craat a splash screen
        loop = QEventLoop(self)
        QTimer.singleShot(2000, loop.quit)
        loop.exec()

    def shareSignal(self):
        self.stackedWidget.currentChanged.connect(self.scollToItem)
        self.ListInterface.tableWidget.itemDoubleClicked.connect(
            self.switchSong)
        self.ListInterface.pushButton.clicked.connect(
            self.ListInterface.initWindow)
        self.musicInterface.pushButtonNext.released.connect(
            lambda: self.nextSong(1))
        self.musicInterface.pushButtonPast.released.connect(
            lambda: self.nextSong(-1))
        self.musicInterface.player.playbackStateChanged.connect(
            lambda: self.nextSong(1, True))

    def setQss(self):
        setTheme(cfg.theme)
        self.windowEffect.removeBackgroundEffect(self.winId())
        if cfg.effect.value == "Mica":
            self.setMicaEffectEnabled(True)
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        elif cfg.effect.value == "Acrylic":
            if isDarkTheme():
                self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F299")
            else:
                self.windowEffect.setAcrylicEffect(self.winId())
        self.setBackgroundColor(self._normalBackgroundColor())

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        # self.setMicaEffectEnabled(False)
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        setTheme(theme)

        # self.setQss()

    def scollToItem(self):
        ''' Scoll to the latest item '''
        if self.stackedWidget.currentIndex() == self.stackedWidget.indexOf(self.ListInterface):
            tabel = self.ListInterface.tableWidget
            tabel.scrollToItem(tabel.currentItem())

    def initNavigation(self):
        # self.addSubInterface(self.searchInterface, FluentIcon.SEARCH, 'Search')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, "播放页")
        self.addSubInterface(self.ListInterface, FIF.ALBUM, "播放列表")
        self.addSubInterface(self.settingInterface, FIF.SETTING,
                             "设置", NavigationItemPosition.BOTTOM)
        self.switchTo(self.musicInterface)

    def initWindow(self):
        self.setWindowIcon(QIcon(r"resource\icon\player.ico"))
        self.setWindowTitle("Mind Player")
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def switchSong(self, item: QTableWidgetItem):
        '''列表双击响应事件'''
        songPath = self.ListInterface.songPosition
        songinfo = self.ListInterface.songInfos
        self.index = item.row()
        # turn to the musicInterface
        self.musicInterface.switchSong(
            songPath[self.index], songinfo[self.index], self.index)
        self.switchTo(self.musicInterface)
        # add title to the tooltip of tray
        self.tray.setToolTip(self.windowTitle() + " - " +
                             songinfo[self.index][0])

    def nextSong(self, distance: int, isAuto: bool = False):
        # "isAuto" is for recongize whether the function is actived by the button or a stop signal
        if self.musicInterface.fp == "":
            return
        if isAuto and self.musicInterface.isplay:
            return
        songPath = self.ListInterface.songPosition
        songinfo = self.ListInterface.songInfos
        playmode = self.musicInterface.playMode
        table = self.ListInterface.tableWidget

        if playmode == PlayMode.order:
            self.index += distance

        elif playmode == PlayMode.random:
            new = random.randint(0, len(songPath)-1)
            while new == self.index:
                new = random.randint(0, len(songPath)-1)
            self.index = new

        elif playmode == PlayMode.single:
            if not isAuto:
                self.index += distance

        elif playmode == PlayMode.repeat:
            self.index += distance
            if self.index >= len(songPath):
                self.index = 0

        try:
            self.musicInterface.switchSong(
                songPath[self.index], songinfo[self.index], self.index)
            table.setCurrentItem(table.item(self.index, 0))
        except IndexError:
            InfoBar.error("", "已经到极限了！", parent=self.musicInterface)
            self.index -= distance

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()


class tray(QSystemTrayIcon):
    def __init__(self, window: Main):
        super().__init__()
        self.window = window
        self.setIcon(self.window.windowIcon())
        self.setToolTip(self.window.windowTitle())

        self.menu = SystemTrayMenu(self.window)
        self.setContextMenu(self.menu)
        self.action = [
            Action("⏸️    暂停",
                   triggered=self.window.musicInterface.player.pause),
            Action("▶️       播放",
                   triggered=self.window.musicInterface.player.play),
            Action("        退出",
                   triggered=exit)
        ]
        self.menu.addActions(self.action)
        self.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.window.isHidden():
                self.window.show()
            elif self.window.isMinimized():
                self.window.showNormal()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    fluentTranslator = FluentTranslator(locale)
    settingTranslator = QTranslator()
    settingTranslator.load(locale, "settings", ".", "resource/i18n")

    app.installTranslator(fluentTranslator)
    app.installTranslator(settingTranslator)

    # create main window
    w = Main()
    w.show()
    app.exec()
