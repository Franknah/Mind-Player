from PySide6.QtWidgets import (QWidget, QTableWidgetItem,
                               QAbstractItemView, QHBoxLayout, QFrame,
                               QApplication)
from resource.ui.Ui_list import Ui_Form
from PySide6.QtCore import Qt, Slot, Signal, QObject
from qfluentwidgets import (isDarkTheme, Theme,
                            setTheme, NavigationItemPosition, FluentIcon,
                            InfoBar)
from config import cfg
import sys
import os
from mutagen.mp3 import MP3
from mutagen import id3


class PlayList(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setObjectName("List")
        self.ui.pushButton.setIcon(FluentIcon.UPDATE)
        self.ui.pushButton.clicked.connect(self.initWindow)

        self.initWindow()

        self.__connectSignalToSlot()

    def initWindow(self):
        try:
            self.songInfos, self.songPosition = self.getMp3info(
                cfg.musicFolders.value)
        except PermissionError:
            InfoBar.error("权限错误", "没有足够的权限", parent=self)
        self.ui.tableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableWidget.setWordWrap(False)
        self.ui.tableWidget.setRowCount(len(self.songInfos))
        self.ui.tableWidget.setColumnCount(4)

        for i, songInfo in enumerate(self.songInfos):
            for j in range(4):
                self.ui.tableWidget.setItem(
                    i, j, QTableWidgetItem(songInfo[j]))
        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['标题', '艺术家', '专辑', '时长'])
        self.ui.tableWidget.resizeColumnsToContents()
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

    def getMp3info(self, directories: list):
        all_files = []
        all_paths = []
        for directory in directories:
            for filename in os.listdir(directory):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(directory, filename)
                    all_paths.append(filepath)
                    audio = MP3(filepath)
                    title = audio.get('TIT2', 'Unknown Title')
                    artist = audio.get('TPE1', 'Unknown Artist')
                    album = audio.get('TALB', 'Unknown Album')
                    length_in_seconds = int(audio.info.length)
                    minutes, seconds = divmod(length_in_seconds, 60)
                    length = f"{minutes:02d}:{seconds:02d}"
                    if not isinstance(title, str):
                        title = title.text[0]
                    if not isinstance(artist, str):
                        artist = artist.text[0]
                    if not isinstance(album, str):
                        album = album.text[0]
                    all_files.append([title, artist, album, length])
        return all_files, all_paths


if __name__ == '__main__':
    # print(get_supported_mime_types())
    app = QApplication(sys.argv)
    w = PlayList()
    w.show()
    sys.exit(app.exec())
