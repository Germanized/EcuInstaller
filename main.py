import sys
import os
import urllib.request
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QPoint, QRectF

class InstallerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.dragging = False
        self.drag_start_position = QPoint()

    def init_ui(self):
        layout = QVBoxLayout()

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
            QLineEdit {
                background-color: #3e3e3e;
                border: 1px solid #555555;
                border-radius: 5px;
                color: #ffffff;
                padding: 5px;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #666666;
                border-radius: 5px;
                color: #ffffff;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)

        title = QLabel('Minecraft Essential Unlocker Mod Installer')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.ecu_path = QLineEdit(self)
        self.ecu_path.setPlaceholderText('Path to ecu-1.4.0.jar')
        layout.addWidget(self.ecu_path)

        btn_browse_ecu = QPushButton('Browse for ecu-1.4.0.jar', self)
        btn_browse_ecu.clicked.connect(self.browse_ecu)
        layout.addWidget(btn_browse_ecu)

        self.essential_path = QLineEdit(self)
        self.essential_path.setPlaceholderText('Path to Essential Mod (fabric_1.x.x).jar')
        layout.addWidget(self.essential_path)

        btn_browse_essential = QPushButton('Browse for Essential Mod', self)
        btn_browse_essential.clicked.connect(self.browse_essential)
        layout.addWidget(btn_browse_essential)

        btn_install = QPushButton('Install Mods', self)
        btn_install.clicked.connect(self.install_mods)
        layout.addWidget(btn_install)

        credits = QLabel('Credits to github.com/Germanized')
        credits.setAlignment(Qt.AlignCenter)
        credits.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(credits)

        self.setLayout(layout)
        self.setWindowTitle('Minecraft Mod Installer')
        self.setGeometry(300, 300, 600, 400)  

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
        radius = 13

        path = QPainterPath()
        rect = QRectF(self.rect())  
        path.addRoundedRect(rect, radius, radius)

        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)  

    def browse_ecu(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select ecu-1.4.0.jar', '', 'JAR Files (*.jar)')
        if file:
            self.ecu_path.setText(file)

    def browse_essential(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select Essential Mod', '', 'JAR Files (*.jar)')
        if file:
            self.essential_path.setText(file)

    def install_mods(self):
        ecu_jar = self.ecu_path.text()
        essential_jar = self.essential_path.text()

        if not os.path.isfile(ecu_jar) or not os.path.isfile(essential_jar):
            QMessageBox.critical(self, 'Error', 'Please provide valid paths for both JAR files.')
            return

        minecraft_path = QFileDialog.getExistingDirectory(self, 'Select Minecraft Directory')
        if not minecraft_path:
            QMessageBox.critical(self, 'Error', 'Please select the Minecraft directory.')
            return

        mods_folder = os.path.join(minecraft_path, 'mods')
        essential_folder = os.path.join(minecraft_path, 'essential')

        os.makedirs(mods_folder, exist_ok=True)
        os.makedirs(essential_folder, exist_ok=True)

        os.system(f'copy "{essential_jar}" "{mods_folder}"')

        ecu_url = 'https://github.com/dxxxxy/EssentialCosmeticsUnlocker/releases/download/1.4.0/ecu-1.4.0.jar'
        ecu_local_path = os.path.join(mods_folder, 'ecu-1.4.0.jar')
        urllib.request.urlretrieve(ecu_url, ecu_local_path)

        QMessageBox.information(self, 'Success', 'Mods installed successfully!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = InstallerGUI()
    installer.setWindowShape()  
    installer.show()
    sys.exit(app.exec_())
