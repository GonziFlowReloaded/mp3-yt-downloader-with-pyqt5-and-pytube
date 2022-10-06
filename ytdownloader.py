
import imp
from logging import exception
import time
import moviepy.editor as mp

import os
from PyQt5 import uic, QtWebEngineWidgets, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QMainWindow, QProgressBar
from PyQt5.QtCore import Qt, QThread
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
        video = yt.streams.get_by_itag("251")
        
        destination = os.path.join(os.getcwd(), "Descargas")
        if not os.path.exists(destination):
            os.makedirs(destination)
        
        out_file = video.download(destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"

        os.replace(out_file, new_file)
        
        QMessageBox.information(self, "Descarga", "Descarga completada")
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def iniciarBarraProgreso(self):
        self.hilo = Hilo()
        self.hilo.chv.connect(self.actualizarBarraProgreso)
        self.hilo.start()
    def actualizarBarraProgreso(self, valor):
        self.barraProgreso.setValue(valor)
        if valor == 100:
            self.labelCargado.setText("Descarga completada")
            self.botonDescarga.setEnabled(False)

class Hilo(QThread):
    chv=QtCore.pyqtSignal(int)
    def run(self):
        contador = 0
        while contador < 100:
            cont+=4
            time.sleep(0.1)
            self.chv.emit(contador)

if "__main__" == __name__:
    app = QApplication(sys.argv)
    wi = PROGRAMA()
    wi.show()
    app.exec_()