import PySide6.QtGui
from PySide6.QtWidgets import (QWidget, QTableWidgetItem, QTableWidget,
                               QAbstractItemView, QHBoxLayout, QFrame,
                               QApplication, QTableView)
from resource.ui.list_ui import Ui_Form
from PySide6.QtCore import Qt
from PySide6.QtGui import QContextMenuEvent, QMouseEvent
from qfluentwidgets import (isDarkTheme, Theme,
                            setTheme, NavigationItemPosition, FluentIcon,
                            InfoBar, RoundMenu, Action, MenuAnimationType)
from config import cfg
import sys
import os

from Parser import Music
from mutagen import File


class PlayList(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName("List")
        self.pushButton.setIcon(FluentIcon.UPDATE)
        self.pushButton.clicked.connect(self.initWindow)
        self.tableWidget.mousePressEvent = self.pressEvent
        # self.tableWidget.mouseReleaseEvent = self.releaseEvent
        self.initWindow()

        self.__connectSignalToSlot()

    def initWindow(self):
        try:
            self.songInfos, self.songPosition = self.getMusicinfo(
                cfg.musicFolders.value)
        except PermissionError:
            InfoBar.error("权限错误", "没有足够的权限", parent=self)

        self.initTabel()

    def initTabel(self):
        self.tableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setRowCount(len(self.songInfos))
        self.tableWidget.setColumnCount(4)

        for i, songInfo in enumerate(self.songInfos):
            for j in range(4):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(songInfo[j]))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setHorizontalHeaderLabels(
            ['标题', '艺术家', '专辑', '时长'])
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.setQss()

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{color}/list.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)
        self.setQss()

    def __connectSignalToSlot(self):
        """ connect signal to slot """

        cfg.themeChanged.connect(self.__onThemeChanged)

    def pressEvent(self, e: QMouseEvent):
        return QTableView.mousePressEvent(self.tableWidget, e)



    def getMusicinfo(self, directories: list):
        infos = []
        paths = []
        for directory in directories:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if not File(filepath):
                    continue
                paths.append(filepath)
                audio = Music(filepath)
                infos.append([audio.Title,
                              audio.Artist,
                              audio.Album,
                              audio.Length,
                              audio.path,
                              audio.Year,
                              audio.Track])
        return infos, paths


if __name__ == '__main__':
    # print(get_supported_mime_types())
    app = QApplication(sys.argv)
    w = PlayList()
    w.show()
    sys.exit(app.exec())
