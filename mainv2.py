import sys
import os
import urllib.request
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QPalette, QColor, QPainter, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QPoint, QTimer, QRectF

class RoundedProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #2e2e2e;  
                border-radius: 20px;
                height: 40px;  
            }
            QProgressBar::chunk {
                background-color: #ffffff;  
                border-radius: 20px;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        chunk_width = int((self.value() / self.maximum()) * rect.width())

        painter.setBrush(QColor(46, 46, 46))  
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

        fill_rect = QRectF(rect.adjusted(0, 0, chunk_width, 0))
        painter.setBrush(QColor(255, 255, 255))  
        painter.drawRoundedRect(fill_rect, 20, 20)

class InstallerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.dragging = False
        self.drag_start_position = QPoint()
        self.loading_timer = QTimer()
        self.loading_value = 0

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(40, 44, 52))
        palette.setColor(QPalette.Foreground, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setStyleSheet("""
            QWidget {
                border-radius: 15px;
                background-color: #2e2e2e;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #666666;
                border-radius: 15px;
                color: #ffffff;
                padding: 10px 15px;  /* Adjusted padding */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)

        title = QLabel('Essential Unlock All Installer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        progress_container = QWidget()
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setAlignment(Qt.AlignCenter)
        self.loading_bar = RoundedProgressBar()
        self.loading_bar.setMaximum(100)
        self.loading_bar.setValue(0)
        progress_layout.addWidget(self.loading_bar)
        progress_container.setLayout(progress_layout)
        layout.addWidget(progress_container)

        self.start_button = QPushButton('Start Install')
        self.start_button.clicked.connect(self.start_installation)
        layout.addWidget(self.start_button)

        credits = QLabel('Developed by Github.com/Germanized')
        credits.setAlignment(Qt.AlignCenter)
        credits.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(credits)

        self.setLayout(layout)
        self.setWindowTitle('Minecraft Mod Installer')
        self.setGeometry(300, 300, 600, 250)  

        self.setWindowShape()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 30:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_start_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def setWindowShape(self):
        radius = 15

        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, radius, radius)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def start_installation(self):
        self.start_button.setDisabled(True)
        self.loading_value = 0
        self.loading_timer.timeout.connect(self.update_loading_bar)
        self.loading_timer.start(50)  

        self.check_paths()

    def update_loading_bar(self):
        self.loading_value += 1
        self.loading_bar.setValue(self.loading_value)
        if self.loading_value >= 100:
            self.loading_timer.stop()
            self.install_mods()

    def check_paths(self):
        user_home = os.path.expanduser("~")
        minecraft_path = os.path.join(user_home, 'AppData', 'Roaming', '.minecraft')

        if not os.path.exists(minecraft_path):
            self.show_path_error("We did not find your Minecraft path. Would you like to select it?")
        else:
            essential_path = os.path.join(minecraft_path, 'essential')
            if not os.path.exists(essential_path):
                self.show_path_error("We did not find your Essential path. Would you like to select it?")
            else:
                self.install_mods()

    def show_path_error(self, message):
        response = QMessageBox.question(self, 'Path Not Found', message,
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if response == QMessageBox.Yes:
            file_dialog = QFileDialog(self, "Select Directory")
            file_dialog.setFileMode(QFileDialog.Directory)
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            if file_dialog.exec_():
                selected_path = file_dialog.selectedFiles()[0]
                if os.path.exists(selected_path):
                    self.install_mods()
                else:
                    QMessageBox.information(self, 'Error', 'Path not found. Installation aborted.')
        else:
            QMessageBox.information(self, 'Error', 'Sorry, if you don\'t supply the path we can\'t install the mod.')

    def install_mods(self):
        user_home = os.path.expanduser("~")
        minecraft_path = os.path.join(user_home, 'AppData', 'Roaming', '.minecraft')
        mods_folder = os.path.join(minecraft_path, 'mods')
        essential_folder = os.path.join(minecraft_path, 'essential')

        os.makedirs(mods_folder, exist_ok=True)
        os.makedirs(essential_folder, exist_ok=True)

        ecu_url = 'https://github.com/dxxxxy/EssentialCosmeticsUnlocker/releases/download/1.4.0/ecu-1.4.0.jar'
        ecu_local_path = os.path.join(mods_folder, 'ecu-1.4.0.jar')

        try:
            urllib.request.urlretrieve(ecu_url, ecu_local_path)
            QMessageBox.information(self, 'Success', 'Mods installed successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download ECU: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = InstallerGUI()
    installer.show()
    sys.exit(app.exec_())
