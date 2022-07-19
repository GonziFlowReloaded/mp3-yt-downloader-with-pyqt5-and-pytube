

import os
from PyQt5 import uic, QtWebEngineWidgets, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QMainWindow
import sys
from pytube import YouTube
#Importar 
class PROGRAMA (QMainWindow):
    def __init__(self):
        super().__init__()
        self.linkardo = ""
        uic.loadUi('interfaz.ui', self)
        self.labelCargado.setText("")
        self.botonDescarga.setEnabled(False)
        self.setWindowTitle("YT Downloader")
        self.cargaLink.clicked.connect(self.cargarLink)
        self.botonDescarga.clicked.connect(self.descargar)
    

    def cargarLink(self):
        try:
            self.linkardo = self.entryLink.text()
            self.labelCargado.setText("Link cargado")
            self.botonDescarga.setEnabled(True)
        except:
            print("Error")

    def descargar(self):
        yt = YouTube(self.linkardo)
        video = yt.streams.filter(only_audio=True).first()
        destination = os.path.join(os.getcwd(), "Descargas")
        if not os.path.exists(destination):
            os.makedirs(destination)
        out_file = video.download(destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)
        
        QMessageBox.information(self, "Descarga", "Descarga completada")
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if "__main__" == __name__:
    app = QApplication(sys.argv)
    wi = PROGRAMA()
    wi.show()
    app.exec_()