from PySide6.QtWidgets import (
    QWidget, QTableWidgetItem, QAbstractItemView, QApplication, QTableView)
from PySide6.QtCore import Qt
from resource.ui.list_ui import Ui_Form
from PySide6.QtGui import QMouseEvent
from qfluentwidgets import (
    isDarkTheme, Theme, setTheme, FluentIcon, InfoBar, Dialog, LineEdit, ComboBox,
    PrimaryPushButton)
from config import cfg
import sys
import os

from Parser import Music
from mutagen import File


class EditDialog(Dialog):

    def __init__(self, title, content, row, parent=None):
        super().__init__(title, content, parent)
        self.saveButton = PrimaryPushButton('保存', self.buttonGroup)
        self.buttonLayout.addWidget(
            self.saveButton, 1, Qt.AlignmentFlag.AlignVCenter)
        self.row = row
        self.comboBox = ComboBox()
        self.comboBox.addItems(['标题', '艺术家', '专辑', '年份'])
        self.lineEdit = LineEdit()
        self.lineEdit.setPlaceholderText('请输入内容')
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()
        self.lineEdit.setFixedWidth(300)
        self.textLayout.addWidget(self.comboBox)
        self.textLayout.addWidget(self.lineEdit)
        self.setTitleBarVisible(False)
        self.comboBox.currentTextChanged.connect(self.textChanged)
        self.saveButton.clicked.connect(
            lambda: parent.editInfo(Music(parent.songPosition[row])))  # 保存(未刷新)
        self.textChanged()

    def textChanged(self):
        self.lineEdit.setText(
            self.parent().tableWidget.item(self.row, self.comboBox.currentIndex()).text()
        )
        self.lineEdit.setFocus()
        self.lineEdit.selectAll()


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
        '''refresh the page'''
        try:
            self.songInfos, self.songPosition = self.getMusicinfo(
                cfg.musicFolders.value)
        except PermissionError:
            InfoBar.error("权限错误", "没有足够的权限", parent=self)
        self.initTabel()

    def initTabel(self):
        '''refresh the tabel'''
        self.tableWidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setRowCount(len(self.songInfos))
        self.tableWidget.setColumnCount(5)

        for i, songInfo in enumerate(self.songInfos):
            for j in range(5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(songInfo[j]))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setHorizontalHeaderLabels(
            ['标题', '艺术家', '专辑', "年份", '时长'])
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
                if not File(filepath):  # 排除音乐文件
                    continue
                paths.append(filepath)
                audio = Music(filepath)
                infos.append(
                    [audio.Title,
                     audio.Artist,
                     audio.Album,
                     audio.Year,
                     audio.Length,
                     audio.path,
                     audio.Track])
        return infos, paths

    def creatDialog(self, index: int):
        toEdit = Music(self.songPosition[index])
        self.dialog = EditDialog("编辑信息", "选择信息", index, self)
        if self.dialog.exec():
            self.editInfo(toEdit)
        self.initWindow()

    def editInfo(self, toEdit: Music):
        try:
            text = self.dialog.lineEdit.text()
            if text.replace(" ", "") == "":  # 排除空情况
                return
            match self.dialog.comboBox.text():
                case "标题":
                    toEdit.Title = text
                case "艺术家":
                    toEdit.Artist = text
                case "专辑":
                    toEdit.Album = text
                case "年份":
                    toEdit.Year = text
            toEdit.id.save()
            InfoBar.success(self.tr("成功"), self.tr("修改成功"), parent=self)
        except:
            InfoBar.error(self.tr("错误"), self.tr("输入错误"), parent=self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PlayList()
    w.show()
    sys.exit(app.exec())
