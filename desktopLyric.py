from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
import PySide6.QtGui
from PySide6.QtWidgets import QApplication,QVBoxLayout
from qframelesswindow import FramelessDialog
from qfluentwidgets import SubtitleLabel

class LyricWindow(FramelessDialog):
    def __init__(self):
        super().__init__()
        self.resize(800,150)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowOpacity(0.8)
        self.setLayout(QVBoxLayout())
        self.enable= False
        self.lrcLabel=SubtitleLabel('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        self.lrcLabel.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.lrcLabel)
    # def mouseMoveEvent(self, event: QMouseEvent) -> None:
    #     event.ignore()
    #     self.move(event.globalPosition().toPoint() - self.pos())
    def mousePressEvent(self, event):
        # 鼠标左键按下时获取鼠标坐标
        if event.button() == Qt.MouseButton.LeftButton:
            self._move_drag = True
            self.m_Position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        # 鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.MouseButton.LeftButton and self._move_drag:
            self.move(event.globalPosition().toPoint() - self.m_Position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # 鼠标按键释放时,取消移动
        self._move_drag = False
    def closeEvent(self,e):
        e.ignore()
        self.enable=False
        self.hide()
    def showEvent(self, e) -> None:
        self.enable=True
        return super().showEvent(e)
    def showLyric(self,lrc):
        if self.enable:
            self.lrcLabel.setText(lrc)
        
if __name__ == '__main__':
    app=QApplication([])
    w=LyricWindow()
    w.show()
    app.exec()