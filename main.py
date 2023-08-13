import os,sys,random
from qframelesswindow import WindowEffect
from qfluentwidgets import (
                            NavigationItemPosition,FluentIcon as FIF,isDarkTheme,
                            FluentTranslator,Theme,setTheme,SplashScreen,InfoBar,
                            FluentWindow,SystemTrayMenu,Action)
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QSystemTrayIcon,QMenu
from player   import MyAudioPlayer,PlayMode
from list import PlayList
from config import cfg
from PySide6.QtGui import QIcon,QAction
from setting_interface import SettingInterface
from PySide6.QtCore import (Qt,QTranslator,Slot,QSize,QTimer,QEventLoop)



class Main(FluentWindow):

    def __init__(self):
        super().__init__()
    

        self.setMinimumSize(800,600)
        self.navigationInterface.setWindowOpacity(0.7)
        self.initWindow()
        self.wscreen=SplashScreen(self.windowIcon(),self,True)
        self.wscreen.setIconSize(QSize(102,102))
        self.show()
        self.createSubInterface()
        self.index = 0
        # self.setQss()
        cfg.themeChanged.connect(self.__onThemeChanged)
        self.musicInterface = MyAudioPlayer()
        self.ListInterface = PlayList()
        self.settingInterface = SettingInterface()
        cfg.micaChanged.connect(self.__onMicaChanged)
        self.stackedWidget.currentChanged.connect(self.scollToItem)
        self.ListInterface.ui.tableWidget.itemDoubleClicked.connect(self.switchSong)
        self.ListInterface.ui.pushButton.clicked.connect(self.ListInterface.initWindow)
        self.musicInterface.ui.pushButtonNext.released.connect(lambda:self.nextSong(1))
        self.musicInterface.ui.pushButtonPast.released.connect(lambda:self.nextSong(-1))
        self.musicInterface.player.playbackStateChanged.connect(lambda:self.nextSong(1,True))
        self.initNavigation()
        self.wscreen.finish()
  
        # add items to navigation interface
    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()


    def setQss(self):
        self.setTheme(cfg.theme.value)
        self.setMicaEffectEnabled(cfg.mica.value)
        # color = 'dark' if isDarkTheme() else 'light'
        #  with open(f'resource\qss\{color}\window.qss', encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())
        
        # self.setStyleSheet("background:grey")   

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        # self.setMicaEffectEnabled(False)
        self.windowEffect.setMicaEffect(self.winId(),isDarkTheme())
        setTheme(theme)
        # self.setQss()
    def __onMicaChanged(self, mica: bool):
        """ mica changed slot """
        self.setMicaEffectEnabled(mica)

    def scollToItem(self):
        if self.stackedWidget.currentIndex()==1:
            tabel=self.ListInterface.ui.tableWidget
            tabel.scrollToItem(tabel.currentItem())
    def initNavigation(self):
        # self.addSubInterface(self.searchInterface, FluentIcon.SEARCH, 'Search')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, "播放页")
        self.addSubInterface(self.ListInterface, FIF.ALBUM, "播放列表")
        self.addSubInterface(self.settingInterface,FIF.SETTING,"设置",NavigationItemPosition.BOTTOM)
        self.switchTo(self.musicInterface)
    def initWindow(self):
        self.setWindowIcon(QIcon(r"resource\icon\player.ico"))
        self.setWindowTitle("Mind Player")
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    def switchSong(self,item:QTableWidgetItem):
        '''列表双击响应事件'''
        songPath=self.ListInterface.songPosition
        songinfo=self.ListInterface.songInfos
        self.index = item.row()
        #向播放页传入参数
        self.musicInterface.switchSong(songPath[self.index],songinfo[self.index],self.index)
        self.switchTo(self.musicInterface)
    def nextSong(self,distance:int,isAuto:bool=False):
        #isAuto用来检验是否是程序自动发出或用户操作
        if self.musicInterface.fp=="":
            return
        if isAuto and self.musicInterface.isplay:
            return
        songPath=self.ListInterface.songPosition
        songinfo=self.ListInterface.songInfos
        if self.musicInterface.playMode==PlayMode.order:
            self.index += distance
        elif self.musicInterface.playMode==PlayMode.random:
            new=random.randint(0,len(songPath)-1)
            while new==self.index:
                new=random.randint(0,len(songPath)-1)
            self.index=new
        elif self.musicInterface.playMode==PlayMode.single:
            pass
        elif self.musicInterface.playMode==PlayMode.repeat:
            self.index += distance
            if self.index>=len(songPath):
                self.index=0  
        try:
            self.musicInterface.switchSong(songPath[self.index],songinfo[self.index],self.index)
            self.ListInterface.ui.tableWidget.setCurrentItem(self.ListInterface.ui.tableWidget.item(self.index,0))
        except IndexError:
            InfoBar.error("","已经到极限了！",parent=self.musicInterface)
            self.index-=distance
    

    # def switchTo(self, widget):
    #     self.tackWidget.setCurrentWidget(widget)
    #     if widget==self.ListInterface:
    #         tabel = self.ListInterface.ui.tableWidget
    #         tabel.setCurrentItem(tabel.item(self.index,0))
    #         tabel.scrollToItem(tabel.currentItem())


    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

        
        
class tray(QSystemTrayIcon):
    def __init__(self,window:Main):
        super().__init__()
        self.window=window
        self.setIcon(QIcon(r"resource/icon/player.ico"))
        self.setToolTip(self.window.windowTitle())

        self.menu=SystemTrayMenu(self.window)
        self.setContextMenu(self.menu)
        self.action=[
            Action("⏸️    暂停",triggered=w.musicInterface.player.pause),
            Action("        退出",triggered=exit)
                     ]
        self.menu.addActions(self.action)
        self.activated.connect(self.on_tray_activated)
        
    def on_tray_activated(self,reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.window.isHidden():
                self.window.show()
                # self.window.createSubInterface()
                # QTimer.singleShot(10000,self.window.wscreen.finish)
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
    tray=tray(w)
    tray.show()
    w.show()
    app.exec()

