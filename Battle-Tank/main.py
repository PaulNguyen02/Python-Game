import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import pyqtSlot
import subprocess

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Tank Chiến'
        self.left = 10
        self.top = 10
        self.width = 728
        self.height = 410
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Thiết lập biểu tượng cho cửa sổ chính
        icon = QIcon('images/icon.png')
        self.setWindowIcon(icon)

        # Tạo label hiển thị hình ảnh
        label = QLabel(self)
        pixmap = QPixmap('images/background.png')
        label.setPixmap(pixmap)
        label.setGeometry(0, 0, self.width, self.height)

        # Tạo 3 nút chế độ
        btn1 = QPushButton('Đối kháng', self)
        btn1.move(80, 350)
        btn1.clicked.connect(self.on_click_mode1)

        btn2 = QPushButton('Tiêu diệt', self)
        btn2.move(230, 350)
        btn2.clicked.connect(self.on_click_mode2)

        btn3 = QPushButton('Sinh tồn', self)
        btn3.move(380, 350)
        btn3.clicked.connect(self.on_click_mode3)

        # Tạo nút thoát
        btn_exit = QPushButton('Thoát', self)
        btn_exit.move(530, 350)
        btn_exit.clicked.connect(self.on_click_exit)

        self.show()

    @pyqtSlot()
    def on_click_mode1(self):
        subprocess.run(['python', 'doikhang.py'])

    @pyqtSlot()
    def on_click_mode2(self):
        subprocess.run(['python', 'tieudiet.py'])

    @pyqtSlot()
    def on_click_mode3(self):
        subprocess.run(['python', 'sinhton.py'])

    @pyqtSlot()
    def on_click_exit(self):
        # Thoát chương trình
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
