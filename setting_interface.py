# coding:utf-8
from config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, SmoothScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme, FluentTranslator)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths, QTranslator
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog, QHBoxLayout, QApplication
import sys


class SettingInterface(SmoothScrollArea):
    """ Setting interface """

    checkUpdateSig = Signal()
    musicFoldersChanged = Signal(list)
    acrylicEnableChanged = Signal(bool)
    downloadFolderChanged = Signal(str)
    minimizeToTrayChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName("SettingInterface")
        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)
        # music folders
        self.musicInThisPCGroup = SettingCardGroup(
            self.tr("Music on this PC"), self.scrollWidget)
        self.musicFolderCard = FolderListSettingCard(
            cfg.musicFolders,
            self.tr("Local music library"),
            directory=QStandardPaths.writableLocation(
                QStandardPaths.MusicLocation),
            parent=self.musicInThisPCGroup
        )
        self.downloadFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.DOWNLOAD,
            self.tr("Download directory"),
            cfg.get(cfg.downloadFolder),
            self.musicInThisPCGroup
        )

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)

        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.effctCard = ComboBoxSettingCard(
            cfg.effect,
            FIF.TRANSPARENT,
            self.tr('窗口效果'),
            self.tr("在 Mind Player 启用窗口效果"),
            ["云母效果 ", "亚克力效果", "无        "],
            parent=self.personalGroup
        )

        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )

        # online music

        # desktop lyric

        # main panel
        self.mainPanelGroup = SettingCardGroup(
            self.tr('Main Panel'), self.scrollWidget)
        self.minimizeToTrayCard = SwitchSettingCard(
            FIF.MINIMIZE,
            self.tr('Minimize to tray after closing'),
            self.tr('PyQt-Fluent-Widgets will continue to run in the background'),
            configItem=cfg.minimizeToTray,
            parent=self.mainPanelGroup
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup(
            self.tr("Software update"), self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('Open help page'),
            FIF.HELP,
            self.tr('Help'),
            self.tr(
                'Discover new features and learn useful tips about PyQt-Fluent-Widgets'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('Provide feedback'),
            FIF.FEEDBACK,
            self.tr('Provide feedback'),
            self.tr('Help us improve PyQt-Fluent-Widgets by providing feedback'),
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('Check update'),
            FIF.INFO,
            self.tr('About'),
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )
        self.configCard = PrimaryPushSettingCard(
            "打开配置文件",
            FIF.SETTING,
            "配置",
            "打开配置文件以自行配置",
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)

        # add cards to group
        self.musicInThisPCGroup.addSettingCard(self.musicFolderCard)
        self.musicInThisPCGroup.addSettingCard(self.downloadFolderCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.effctCard)

        self.personalGroup.addSettingCard(self.languageCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.mainPanelGroup.addSettingCard(self.minimizeToTrayCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.configCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
        self.expandLayout.addWidget(self.personalGroup)

        self.expandLayout.addWidget(self.mainPanelGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}/setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '',
            self.tr('Configuration takes effect after restart'),
            parent=self.window()
        )

    def __onDeskLyricFontCardClicked(self):
        """ desktop lyric font button clicked slot """
        isOk, font = QFontDialog.getFont(
            cfg.desktopLyricFont, self.window(), self.tr("Choose font"))
        if isOk:
            cfg.desktopLyricFont = font

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)

        # music in the pc
        self.musicFolderCard.folderChanged.connect(
            self.musicFoldersChanged)
        self.downloadFolderCard.clicked.connect(
            self.__onDownloadFolderCardClicked)

        # personalization

        # playing interface

        # main panel
        self.minimizeToTrayCard.checkedChanged.connect(
            self.minimizeToTrayChanged)

        # about
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.configCard.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl.fromLocalFile("config\config.json")))
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))


if __name__ == '__main__':
    class Window(FramelessWindow):

        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.setTitleBar(StandardTitleBar(self))

            self.hBoxLayout = QHBoxLayout(self)
            self.settingInterface = SettingInterface()
            self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.hBoxLayout.addWidget(self.settingInterface)

            self.setWindowIcon(QIcon("resource/logo.png"))
            self.setWindowTitle("PySide6-Fluent-Widgets")

            self.resize(1080, 784)
            desktop = QApplication.primaryScreen().size()
            w, h = desktop.width(), desktop.height()
            self.move(w//2 - self.width()//2, h//2 - self.height()//2)

            self.titleBar.raise_()

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
    w = Window()
    w.show()
    app.exec()
